#!/usr/bin/env python3
"""Cross-reference this repo's rules text against the scraped 6th edition wiki.

The wiki mirror (https://6th.whfb.app, scraped by the 6eWikiScraper project) is
treated as the source of truth. This script never edits anything: it reports what
each catalogue says, what the wiki says, and how confident the match is, so the
edits can be made by hand with targeted Edit calls.

Usage:
    python wiki_xref.py                          # all armies -> reports/
    python wiki_xref.py --only "Vampire Counts.cat"
    python wiki_xref.py --text /magic-item/cursed-book   # XML-ready description
    python wiki_xref.py --stubs                  # Phase G: rules left undescribed

The wiki data directory is found via --wiki, then $WHFB_WIKI_DATA, then a
sibling checkout at ../6eWikiScraper/data.
"""

from __future__ import annotations

import argparse
import difflib
import json
import os
import re
import sys
import unicodedata
import xml.etree.ElementTree as ET
from pathlib import Path

from bsdata import CAT_NS, GST_NS, repo_root, source_files, read_text

# --------------------------------------------------------------------- naming

# Vendored verbatim from whfb6e/indexer.py. The lookup keys in index.json were
# built with this exact folding; any divergence silently turns hits into misses,
# so Wiki.check_normalise() re-verifies the agreement against the index at startup.
_PUNCT = re.compile(r"[^\w\s]")
_WS = re.compile(r"\s+")


def normalise(name: str) -> str:
    text = unicodedata.normalize("NFKD", name or "")
    text = "".join(ch for ch in text if not unicodedata.combining(ch))
    text = text.replace("&", " and ").replace("’", "'").replace("'", "")
    text = _PUNCT.sub(" ", text.casefold())
    return _WS.sub(" ", text).strip()


# Bucket D: BattleScribe display labels, not rules. No wiki text exists for these.
MECHANICAL_TAG = re.compile(
    r"^(?:"
    r"Unit Strength\s+\d+"
    r"|(?:Armour|Ward|Scaly Skin|Regeneration)\s*(?:Save)?\s*\(?\d\+\)?"
    r"|Impact Hits?\s*\(.*\)"
    r"|Flying Unit\s*\(.*\)"
    r"|Level\s+\d+\s+Wizard"
    r"|Single Model"
    r")$",
    re.I,
)

# Wiki `association` values per catalogue. Used only to confirm or flag a match --
# never to restrict the search, because army-book content is often tagged under a
# supplement instead (Dogs of War content is tagged "Regiments of Renown").
ARMY_ASSOC = {
    "Bretonnians.cat": ["Bretonnia"],
    "Chaos Dwarves.cat": ["Chaos Dwarfs"],
    "Daemonic Legions.cat": ["Hordes of Chaos", "Storm of Chaos"],
    "Dark Elves.cat": ["Dark Elves"],
    "Dogs of War.cat": ["Dogs of War", "Regiments of Renown"],
    "Dwarfs.cat": ["Dwarfs"],
    "Forces of Chaos.cat": ["Hordes of Chaos", "Beasts of Chaos", "Storm of Chaos"],
    "High Elves.cat": ["High Elves"],
    "Lizardmen.cat": ["Lizardmen"],
    "Ogre Kingdoms.cat": ["Ogre Kingdoms"],
    "Orcs and Goblins.cat": ["Orcs & Goblins"],
    "Skaven.cat": ["Skaven"],
    "The Empire.cat": ["The Empire"],
    "Tomb Kings.cat": ["Tomb Kings"],
    "Vampire Counts.cat": ["Vampire Counts"],
    "Wood Elves.cat": ["Wood Elves"],
    "Warhammer Fantasy 6th Edition.gst": ["Main Rulebook"],
}

# Ranked as the scraper's indexer ranks them (whfb6e/indexer.py MATCH_RANK).
MATCH_RANK = ("page", "alias", "heading", "term", "child")

# Wiki sections that carry rules text. A catalogue <rule> or magic-item entry
# should resolve into one of these rather than to the unit page that uses it.
RULE_SECTIONS = frozenset({
    "special-rules", "magic-item", "magic-items", "weapons", "spell",
    "spell-lists", "army-lists", "psychology", "close-combat",
})

# Narrower than RULE_SECTIONS, and used only for entries carrying no category.
# Those include mundane equipment, and the wiki files Great Weapon, Crossbow and
# Handgun under "weapons" -- core attacking rules, which this project leaves out.
# Widening this to RULE_SECTIONS pulled in 249 such entries.
UNCATEGORISED_OK = frozenset({"magic-item", "magic-items", "spell", "spell-lists",
                              "special-rules"})

MAGIC_CATS = (
    "magic weapon", "magic armour", "magic banner", "magic standard", "talisman",
    "arcane item", "enchanted item", "magic item", "daemonic gift", "virtue",
    "gift", "rune", "spite", "honour", "big name", "venom", "vow",
)


def find_wiki(arg):
    for cand in (arg, os.environ.get("WHFB_WIKI_DATA")):
        if cand:
            p = Path(cand).resolve()
            if (p / "index.json").is_file():
                return p
            sys.exit("no index.json under {}".format(p))
    sib = repo_root().parent / "6eWikiScraper" / "data"
    if (sib / "index.json").is_file():
        return sib.resolve()
    sys.exit("wiki data not found: pass --wiki, or set $WHFB_WIKI_DATA")


class Wiki:
    """Read-only view of the scraper's index.json plus its Markdown pages."""

    def __init__(self, root):
        self.root = root
        data = json.loads((root / "index.json").read_text(encoding="utf-8"))
        self.pages = data["pages"]
        self.lookup = data["lookup"]
        self.build_id = data.get("build_id") or "(offline rebuild - none recorded)"
        self.page_count = data.get("page_count", "?")
        self.generated_at = data.get("generated_at", "?")
        self._keys = list(self.lookup)

    def check_normalise(self):
        """Confirm the vendored normalise() still agrees with the index."""
        bad = []
        for rec in list(self.pages.values())[:400]:
            if rec.get("kind") in ("rule", "magic-item", "spell"):
                key = normalise(rec["name"])
                if key and key not in self.lookup:
                    bad.append((rec["name"], key))
        if len(bad) > 8:
            sys.exit(
                "vendored normalise() disagrees with index.json ({} of 400 sampled "
                "names do not resolve, e.g. {}). Re-copy it from whfb6e/indexer.py."
                .format(len(bad), bad[:3])
            )

    def assoc(self, path):
        a = (self.pages.get(path) or {}).get("association") or []
        return [a] if isinstance(a, str) else list(a)

    def section(self, path):
        return (self.pages.get(path) or {}).get("section", "")

    def text(self, path):
        rec = self.pages.get(path)
        if not rec:
            raise KeyError(path)
        body = (self.root / rec["file"]).read_text(encoding="utf-8")
        if body.startswith("---\n"):
            _, _, body = body.partition("\n---\n")
        return body.lstrip("\n")

    def fuzzy(self, key, limit=4):
        """Candidates for human review only. Never a basis for an automatic edit."""
        scored = {}
        for cand in self._keys:
            if cand.startswith(key) or key.startswith(cand):
                scored[cand] = 0.9
            elif key in cand or cand in key:
                scored[cand] = max(scored.get(cand, 0), 0.8)
        if not scored:
            for cand in self._keys:
                r = difflib.SequenceMatcher(None, key, cand).ratio()
                if r >= 0.82:
                    scored[cand] = r * 0.7
        top = sorted(scored.items(), key=lambda kv: -kv[1])[:limit]
        return [(self.lookup[k][0]["path"], k, round(s, 2)) for k, s in top]


# ------------------------------------------------------------ catalogue side

def ns_for(path):
    return GST_NS if path.suffix == ".gst" else CAT_NS


def id_lines(text):
    """Map every id in the file to the line it is declared on."""
    out = {}
    for i, line in enumerate(text.splitlines(), 1):
        for m in re.finditer(r'\sid="([0-9a-f]{4}(?:-[0-9a-f]{4}){3})"', line):
            out.setdefault(m.group(1), i)
    return out


def cat_inventory(path):
    """Rules, textless magic-item entries, model profiles and item costs."""
    text = read_text(path)
    lines = id_lines(text)
    ns = "{%s}" % ns_for(path)
    root = ET.fromstring(text)
    parents = {c: p for p in root.iter() for c in p}

    def owner(el):
        p = parents.get(el)
        while p is not None:
            tag = p.tag.split("}")[-1]
            if tag in ("selectionEntry", "infoGroup", "selectionEntryGroup"):
                return "{} <{}>".format(p.get("name") or "?", tag)
            p = parents.get(p)
        return "shared"

    rules = []
    for r in root.iter(ns + "rule"):
        desc = r.find(ns + "description")
        rules.append({
            "name": r.get("name") or "",
            "id": r.get("id") or "",
            "line": lines.get(r.get("id") or "", 0),
            "desc": (desc.text or "") if desc is not None else None,
            "owner": owner(r),
        })

    items, profiles, costs = [], [], []
    for se in root.iter(ns + "selectionEntry"):
        cl = se.find(ns + "categoryLinks")
        cats = [c.get("name", "") for c in (cl if cl is not None else [])]
        is_magic = any(any(m in c.lower() for m in MAGIC_CATS) for c in cats)
        # An upgrade with no categoryLink at all is also a candidate: 57 real
        # magic items (Gromril Great Helm, Collar of Khorne) carry no category,
        # so keying purely on category name skipped them. analyse() then drops
        # any whose match is not rules-bearing, which discards the mundane
        # shields and mounts this lets through.
        uncategorised = not cats
        if se.get("type") == "upgrade" and (is_magic or uncategorised):
            def carries(el):
                return any(el.find(ns + x) is not None and len(el.find(ns + x))
                           for x in ("rules", "profiles", "infoLinks"))

            # An entryLink can carry the rules itself -- the game system's
            # "Power Stones" entry has no rules of its own and hangs them off
            # its link to Power Stone, which displays perfectly well.
            links = se.find(ns + "entryLinks")
            has = carries(se) or any(carries(el) for el in (links if links is not None else []))
            cost = se.find("./{0}costs/{0}cost".format(ns))
            pts = cost.get("value") if cost is not None else None
            if not has:
                items.append({
                    "name": se.get("name") or "", "id": se.get("id") or "",
                    "line": lines.get(se.get("id") or "", 0), "cats": cats,
                })
            if pts is not None:
                costs.append({"name": se.get("name") or "", "pts": pts,
                              "id": se.get("id") or "",
                              "line": lines.get(se.get("id") or "", 0)})

    for pr in root.iter(ns + "profile"):
        chars = {c.get("name"): (c.text or "").strip()
                 for c in pr.iter(ns + "characteristic")}
        profiles.append({"name": pr.get("name") or "", "id": pr.get("id") or "",
                         "line": lines.get(pr.get("id") or "", 0), "chars": chars})

    # A description written by a modifier overrides the stored text at runtime.
    overrides = []
    for m in root.iter(ns + "modifier"):
        if m.get("field") != "description":
            continue
        holder = parents.get(parents.get(m)) if parents.get(m) is not None else None
        overrides.append({
            "rule": (holder.get("name") if holder is not None else "?"),
            "line": lines.get(holder.get("id", "") if holder is not None else "", 0),
            "value": (m.get("value") or "")[:90],
        })

    return {"rules": rules, "items": items, "profiles": profiles,
            "costs": costs, "overrides": overrides}


# ------------------------------------------------- Phase C: wiki page -> text

DROP_SECTIONS = ("Related", "Referenced by", "Special Rules", "Profile", "Base Sizes")

# Two tiers. A STRONG signal is something that only appears in mechanical text:
# dice, measurements, target numbers, characteristics, explicit modifiers. The WEAK
# list is ordinary game nouns, which flavour prose uses just as freely ("These
# beasts overpower their enemies as they charge") -- so weak signals only decide
# the split when no paragraph on the page has a strong one.
STRONG_SIGNAL = re.compile(
    r"""\b\d?D\d\b                       # D6, 2D6, D3
      | \d\s*"                           # a measurement: 18"
      | \b\d+\s*(?:pts|points)\b
      | [+-]\s?\d\b                      # +1 / -1
      | \b\d\+                           # 4+ target numbers
      | \b(?:WS|BS|Ld)\s*\d               # WS4 -- two letters, unambiguous
      | \b(?:S|T|W|I|A|M)\s?\d\b          # S4, T 4. A bare letter must carry a
                                          # digit: under re.I, "a long time"
                                          # would otherwise read as an Attacks
                                          # characteristic and keep the flavour.
      | \b(?:Strength|Toughness|Wounds|Initiative|Attacks|Movement|Leadership)\s+\d
      | \b(?:one\ use\ only|bound\ spell|power\ level|casting\ value
           |re-?rolls?|may\ not|counts\ as|treated\ as|to\ represent\ this)\b
    """,
    re.I | re.X,
)

# A link into a rules section marks a paragraph as mechanical regardless of its
# wording. The scraper resolves these for us, so use them before flattening.
LINK_SIGNAL = re.compile(
    r"\]\(\.\.?/(?:special-rules|magic-items?|psychology|spell|spell-lists"
    r"|weapons|close-combat|shooting|movement)/",
)

WEAK_SIGNAL = re.compile(
    r"""\b(?:save|ward|wound|attacks?|casting|cast|charges?|panic|hate[sd]?|hatred
           |fear|terror|frenzy|stupidity|spell|magic\ missile|models?|unit
           |turn|combat|break\ test|armour|immune|must|may)\b""",
    re.I | re.X,
)


def flatten_tables(body):
    """GFM table -> tab-separated lines, matching the Organ Gun Misfire style."""
    out = []
    for line in body.splitlines():
        s = line.strip()
        if re.match(r"^\|[\s:|-]+\|$", s):
            continue
        if s.startswith("|") and s.endswith("|"):
            cells = [c.strip() for c in s[1:-1].split("|")]
            out.append("\t".join(cells))
        else:
            out.append(line)
    return "\n".join(out)


def wiki_rules_text(md):
    """Convert a wiki page body to a BattleScribe description.

    Returns (rules text, dropped flavour paragraphs). The flavour split is a
    heuristic and is reported so it can be eyeballed, not trusted blindly.
    """
    body = re.sub(r"^#\s+.*$", "", md, count=1, flags=re.M)

    out_lines, skipping = [], False
    for line in body.splitlines():
        h = re.match(r"^##\s+(.*?)\s*$", line)
        if h:
            skipping = h.group(1) in DROP_SECTIONS
            if skipping:
                continue
        if not skipping:
            out_lines.append(line)
    body = "\n".join(out_lines)

    body = flatten_tables(body)
    body = re.sub(r"^#{2,6}\s+", "", body, flags=re.M)
    body = re.sub(r"\*\*(.*?)\*\*", r"\1", body)
    body = re.sub(r"(?<!\*)\*(?!\*)(.+?)(?<!\*)\*(?!\*)", r"\1", body)
    body = re.sub(r"^!\[.*$", "", body, flags=re.M)

    # Classify while the links are still here: a paragraph that links to another
    # rules page is mechanical, whatever words it uses. The Axe of Khorne gift
    # reads "A Daemon with an Axe of Khorne gains the [Killing Blow](...)" --
    # no dice, no measurement, no keyword, but unmistakably the rule. Flattening
    # first threw that signal away and kept the flavour line above it.
    paras = [p.strip() for p in re.split(r"\n\s*\n", body) if p.strip()]
    linked = [bool(LINK_SIGNAL.search(p)) for p in paras]
    paras = [re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", p) for p in paras]

    # Drop leading paragraphs only while they carry NO game vocabulary at all,
    # and stop at the first that does. Cutting to the first STRONG signal was
    # tried and is wrong: the Terror page states three paragraphs of real rules
    # before it reaches a measurement, and all three were being discarded.
    # Keeping a stray line of flavour is cosmetic; dropping rules is a bug.
    first = 0
    while first < len(paras) and not (linked[first]
                                      or STRONG_SIGNAL.search(paras[first])
                                      or WEAK_SIGNAL.search(paras[first])):
        first += 1
    if first == len(paras):          # nothing looked mechanical anywhere
        return "\n\n".join(paras), []
    return "\n\n".join(paras[first:]), paras[:first]


XML_ESCAPES = (("&", "&amp;"), ("<", "&lt;"), (">", "&gt;"),
               ('"', "&quot;"), ("'", "&apos;"))


def xml_escape(s):
    for a, b in XML_ESCAPES:
        s = s.replace(a, b)
    return s


# ---------------------------------------------------------------- classifying

def variants(name):
    """Deterministic rewrites only -- each is named in the report.

    These exist because the catalogues and the wiki disagree on grammar, not on
    identity: "Fiend of Slaanesh" vs "Fiends of Slaanesh", "Prayer of Sigmar"
    vs "Prayers of Sigmar", "Guardian of Sacred Sites" vs "Guardian of the
    Sacred Sites". Renaming the catalogue for these would be wrong -- its name
    is legitimate -- so the matcher learns the shapes instead.

    Spelling differences are deliberately NOT handled here. Some are catalogue
    typos and some are wiki typos (the wiki has "Vitrolic Totem" and "Stone of
    the Crystal Merex"), and guessing which side is right is a judgement for
    the maintainer, not a rewrite rule. Those stay in bucket E.
    """
    n = re.sub(r"\s+", " ", name.strip())
    head = n.split(" ", 1)

    cands = [
        re.sub(r"^The\s+", "", n, flags=re.I),
        "The " + n,
        re.sub(r"\s*\([^)]*\)\s*$", "", n),
        n[:-1] if n.endswith("s") else n + "s",
        re.sub(r"s(\s*\([^)]*\))$", r"\1", n),
        # plural on the head noun: "Fiend of Slaanesh" <-> "Fiends of Slaanesh"
        (head[0] + "s " + head[1]) if len(head) == 2 and not head[0].endswith("s") else n,
        (head[0][:-1] + " " + head[1]) if len(head) == 2 and head[0].endswith("s") else n,
        # the article after "of": "Banner of Zenith" <-> "Banner of the Zenith"
        re.sub(r"\bof the\b", "of", n, flags=re.I),
        re.sub(r"\bof (?!the\b)", "of the ", n, count=1, flags=re.I),
    ]

    seen = set()
    for v in cands:
        v = v.strip()
        if v and v != n and v not in seen:
            seen.add(v)
            yield v


def classify(name, wiki, assocs):
    if MECHANICAL_TAG.match(name.strip()):
        return {"bucket": "D", "hits": [], "via": None}

    def resolve(key, via):
        hits = wiki.lookup.get(key)
        if not hits:
            return None
        if len(hits) == 1:
            return {"bucket": "A", "hits": hits, "via": via}

        # 1. Keep only the strongest match kind: an exact page beats an alias,
        #    which beats a heading inside some larger page.
        best = min(MATCH_RANK.index(h["match"]) if h["match"] in MATCH_RANK else 99
                   for h in hits)
        cands = [h for h in hits
                 if (MATCH_RANK.index(h["match"]) if h["match"] in MATCH_RANK else 99) == best]

        # 2. A <rule> named "Black Guard" means the rule, not the unit that has
        #    it, so prefer sections that carry rules text over unit/army pages.
        ruleish = [h for h in cands if wiki.section(h["path"]) in RULE_SECTIONS]
        if ruleish:
            cands = ruleish

        # 3. Only then fall back to the army the wiki files it under. This runs
        #    on aliases too -- "Hidden" is an alias on both the Dark Elf and the
        #    Skaven page, and association is the only thing that separates them.
        if len(cands) > 1 and assocs:
            conf = [c for c in cands if set(wiki.assoc(c["path"])) & set(assocs)]
            if len(conf) == 1:
                cands = conf

        if len(cands) == 1:
            return {"bucket": "A", "hits": cands, "via": via}
        return {"bucket": "C", "hits": cands, "via": via}

    got = resolve(normalise(name), None)
    if got:
        # An off-army association is a flag, not a veto. Dark Elves.cat carries a
        # block of Chaos items (Armour of Damnation, Banner of Wrath) that the
        # wiki files under Hordes of Chaos; each name is globally unique, so the
        # match is certain and only the provenance is worth a second look.
        # Demoting these to C buried 36 correct matches in one file.
        if got["bucket"] == "A" and assocs:
            a = wiki.assoc(got["hits"][0]["path"])
            if a and not set(a) & set(assocs):
                got["note"] = "wiki files this under {}".format(", ".join(a[:3]))
        return got

    for v in variants(name):
        got = resolve(normalise(v), v)
        if got and got["bucket"] == "A":
            got["bucket"] = "B"
            return got

    return {"bucket": "E", "hits": [], "via": None,
            "candidates": wiki.fuzzy(normalise(name))}


# ------------------------------------------------------------------ reporting

def norm_ws(s):
    return _WS.sub(" ", (s or "").replace("’", "'")).strip().casefold()


def analyse(path, wiki):
    inv = cat_inventory(path)
    assocs = ARMY_ASSOC.get(path.name, [])
    rows = []
    for r in inv["rules"]:
        c = classify(r["name"], wiki, assocs)
        row = dict(r)
        row.update(c)
        row["kind"] = "rule"
        # An ambiguous name whose text already matches one of the candidates is
        # decided, not undecided. Stream of Corruption is two different rules
        # sharing a name; once each element carries the right one there is
        # nothing left to ask, even though the name still resolves to two pages.
        if c["bucket"] == "C" and (r["desc"] or "").strip():
            for h in c["hits"]:
                try:
                    cand, _ = wiki_rules_text(wiki.text(h["path"]))
                except (KeyError, OSError):
                    continue
                if norm_ws(cand) == norm_ws(r["desc"]):
                    c = {"bucket": "A", "hits": [h], "via": None}
                    row.update(c)
                    row.pop("note", None)
                    break
        if c["bucket"] in ("A", "B") and c["hits"]:
            wpath = c["hits"][0]["path"]
            try:
                proposed, flavour = wiki_rules_text(wiki.text(wpath))
            except (KeyError, OSError):
                proposed, flavour = "", []
            row["wiki_path"] = wpath
            row["proposed"] = proposed
            row["flavour"] = flavour
            row["same"] = norm_ws(proposed) == norm_ws(r["desc"])
            # A page that converts to nothing is not a usable match. "The Fay
            # Enchantress" resolves to /unit/the-fay-enchantress, which is a
            # statline and a list of links -- both correctly dropped, leaving
            # an empty description that would overwrite good existing text.
            if not proposed.strip():
                row["bucket"] = "E"
                row["note"] = "{} has no rules text (probably a unit page)".format(wpath)
                row["candidates"] = [(wpath, "", 1.0)]
            # The game system is shared by all 16 catalogues, so only core
            # rulebook content belongs in it. Its bare "Chariot" tag otherwise
            # resolves to Gorthor's chariot - a Beasts of Chaos special
            # character's rule - and would ship that to every army.
            elif path.suffix == ".gst" and "Main Rulebook" not in wiki.assoc(wpath):
                row["bucket"] = "C"
                row["note"] = "{} is {}, not core rulebook - wrong for a shared rule".format(
                    wpath, ", ".join(wiki.assoc(wpath)) or "unattributed")
        rows.append(row)

    for it in inv["items"]:
        c = classify(it["name"], wiki, assocs)
        row = dict(it)
        row.update(c)
        row["kind"] = "item"
        row["desc"] = None
        row["same"] = False
        if c["bucket"] in ("A", "B") and c["hits"]:
            wpath = c["hits"][0]["path"]
            # An uncategorised entry is only a magic item if it resolves to a
            # page that carries rules. Shields, mounts and unit-size options
            # come through the same door and must not pick up a unit page.
            if not it["cats"] and wiki.section(wpath) not in UNCATEGORISED_OK:
                continue
            try:
                proposed, flavour = wiki_rules_text(wiki.text(wpath))
            except (KeyError, OSError):
                proposed, flavour = "", []
            if not proposed.strip():
                continue
            row["wiki_path"] = wpath
            row["proposed"] = proposed
            row["flavour"] = flavour
        elif not it["cats"]:
            continue          # uncategorised and unmatched: not our business
        rows.append(row)
    return inv, rows


def write_report(out_dir, path, wiki, inv, rows):
    buckets = {}
    for r in rows:
        buckets.setdefault(r["bucket"], []).append(r)
    lines = [
        "# {} - wiki cross-reference".format(path.name),
        "",
        "Wiki build `{}`, indexed {}.".format(wiki.build_id, wiki.generated_at),
        "Associations: {}".format(", ".join(ARMY_ASSOC.get(path.name, [])) or "-"),
        "",
        "| Bucket | Rows |", "| --- | ---: |",
    ]
    for b in "ABCDE":
        lines.append("| {} | {} |".format(b, len(buckets.get(b, []))))
    todo = [r for r in rows if r["bucket"] in ("A", "B") and not r.get("same")]
    lines += ["", "**{} rows need an edit** ({} rules, {} textless items).".format(
        len(todo), sum(1 for r in todo if r["kind"] == "rule"),
        sum(1 for r in todo if r["kind"] == "item")), ""]

    offarmy = [r for r in rows if r.get("note") and r["bucket"] in ("A", "B")]
    if offarmy:
        lines += ["## Matched, but filed under another army ({})".format(len(offarmy)),
                  "", "The name is unique on the wiki so the match is certain; only the "
                  "provenance is unusual. Worth a scan, not a decision.", ""]
        for r in sorted(offarmy, key=lambda x: x["line"]):
            lines.append("- **{}** ({}:{}) - {} - `{}`".format(
                r["name"], path.name, r["line"], r["note"], r.get("wiki_path", "?")))
        lines.append("")

    if inv["overrides"]:
        lines += ["## Description modifiers (stored text is not what displays)", ""]
        for o in inv["overrides"]:
            lines.append("- `{}:{}` **{}** -> `{}`".format(
                path.name, o["line"], o["rule"], o["value"]))
        lines.append("")

    for b, title in (("A", "A - exact match"), ("B", "B - deterministic variant"),
                     ("C", "C - ambiguous, needs a decision"),
                     ("E", "E - no wiki coverage"), ("D", "D - mechanical tag, skip")):
        got = buckets.get(b, [])
        if not got:
            continue
        lines += ["---", "", "## {} ({})".format(title, len(got)), ""]
        for r in sorted(got, key=lambda x: x["line"]):
            head = "### {} `{}` - {}:{}".format(r["name"], r["id"], path.name, r["line"])
            lines += [head, ""]
            if r["kind"] == "item":
                lines.append("*textless magic-item entry - needs a new `<rules>` block*")
            if r.get("via"):
                lines.append("matched via variant **{}**".format(r["via"]))
            if r.get("note"):
                lines.append("**{}**".format(r["note"]))
            if b in ("A", "B"):
                lines += ["", "wiki: `{}`".format(r.get("wiki_path", "?")), ""]
                if r.get("same"):
                    lines.append("*already matches - no edit needed*")
                else:
                    if r.get("flavour"):
                        lines += ["<details><summary>dropped flavour ({} para)</summary>".format(
                            len(r["flavour"])), "", "> " + "\n> ".join(
                            " ".join(r["flavour"])[:400].splitlines()), "", "</details>", ""]
                    lines += ["```text", r.get("proposed", "") or "(empty)", "```", ""]
                    if r.get("desc"):
                        lines += ["<details><summary>current text</summary>", "",
                                  "```text", r["desc"], "```", "</details>", ""]
                    elif r["kind"] == "rule":
                        lines.append("*(currently undescribed)*")
            elif b == "C":
                lines.append("")
                for h in r["hits"][:6]:
                    lines.append("- `{}` - {} ({}) assoc {}".format(
                        h["path"], h["name"], h["match"], wiki.assoc(h["path"])[:3]))
            elif b == "E":
                lines.append("")
                for p, k, s in r.get("candidates", []):
                    lines.append("- {:.2f} `{}` (key `{}`) - **not applied**".format(s, p, k))
                if not r.get("candidates"):
                    lines.append("- no candidate at any confidence")
            lines.append("")

    out = out_dir / (path.stem + ".md")
    out.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")
    return buckets, todo


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--wiki", help="scraper data dir (holds index.json)")
    ap.add_argument("--out", default="reports", help="output dir (default: reports/)")
    ap.add_argument("--only", help="one data file, e.g. 'Vampire Counts.cat'")
    ap.add_argument("--text", help="print the XML-ready description for a wiki path")
    ap.add_argument("--stubs", action="store_true",
                    help="Phase G: every rule still without a description")
    ap.add_argument("--numbers", action="store_true",
                    help="Phase F: points-cost and statline differences")
    ap.add_argument("--root", help="repo root (default: auto-detected)")
    args = ap.parse_args()

    root = repo_root(args.root)
    wiki = Wiki(find_wiki(args.wiki))
    wiki.check_normalise()

    if args.text:
        # Git Bash rewrites a leading-slash argument into a Windows path, so
        # accept "magic-items/lahmia" as well as "/magic-items/lahmia".
        wpath = args.text.replace("\\", "/")
        wpath = "/" + wpath.rsplit(":/", 1)[-1].lstrip("/")
        body, flavour = wiki_rules_text(wiki.text(wpath))
        if flavour:
            sys.stderr.write("dropped {} flavour para\n".format(len(flavour)))
        print(xml_escape(body))
        return 0

    files = [p for p in source_files(root) if not args.only or p.name == args.only]
    if not files:
        sys.exit("no such data file: {}".format(args.only))

    out_dir = root / args.out
    out_dir.mkdir(exist_ok=True)

    if args.numbers:
        return write_numbers(out_dir, files, wiki)

    if args.stubs:
        return write_stubs(out_dir, files, wiki)

    totals, summary = {}, []
    for path in files:
        inv, rows = analyse(path, wiki)
        buckets, todo = write_report(out_dir, path, wiki, inv, rows)
        for b in "ABCDE":
            totals[b] = totals.get(b, 0) + len(buckets.get(b, []))
        summary.append((path.name, buckets, todo, inv))
        print("{:36} A{:4} B{:3} C{:3} D{:3} E{:3}   edits {:4}".format(
            path.name, *[len(buckets.get(b, [])) for b in "ABCDE"], len(todo)))

    lines = ["# Wiki cross-reference summary", "",
             "Wiki build `{}`, indexed {}.".format(wiki.build_id, wiki.generated_at), "",
             "| Catalogue | A | B | C | D | E | edits needed |",
             "| --- | ---: | ---: | ---: | ---: | ---: | ---: |"]
    for name, buckets, todo, _ in summary:
        lines.append("| [{0}]({1}.md) | {2} | {3} | {4} | {5} | {6} | {7} |".format(
            name, Path(name).stem, *[len(buckets.get(b, [])) for b in "ABCDE"], len(todo)))
    lines += ["| **total** | {} | {} | {} | {} | {} | **{}** |".format(
        *[totals.get(b, 0) for b in "ABCDE"], sum(len(t) for _, _, t, _ in summary)), ""]
    (out_dir / "summary.md").write_text("\n".join(lines) + "\n",
                                        encoding="utf-8", newline="\n")
    print("\nwrote {}/summary.md".format(args.out))
    return 0


STAT_ORDER = ("M", "WS", "BS", "S", "T", "W", "I", "A", "Ld")


def _best(wiki, name, kind):
    """The single wiki page of this kind whose name matches, or None."""
    hits = wiki.lookup.get(normalise(name)) or []
    pages = [h for h in hits if h["kind"] == kind and h["match"] == "page"]
    return pages[0]["path"] if len(pages) == 1 else None


def write_numbers(out_dir, files, wiki):
    """Phase F: report numeric differences. Reports only -- changes nothing."""
    cost_rows, stat_rows = [], []
    for path in files:
        inv = cat_inventory(path)
        for c in inv["costs"]:
            wpath = _best(wiki, c["name"], "magic-item")
            if not wpath:
                continue
            want = (wiki.pages[wpath] or {}).get("points_cost")
            if want is None:
                continue
            try:
                have = float(c["pts"])
            except (TypeError, ValueError):
                continue
            if abs(have - float(want)) > 0.001:
                cost_rows.append((path.name, c["name"], c["line"], have, want,
                                  abs(have - float(want)), wpath))
        for pr in inv["profiles"]:
            wpath = _best(wiki, pr["name"], "unit")
            if not wpath:
                continue
            stats = (wiki.pages[wpath] or {}).get("statistics") or {}
            if not stats:
                continue
            # Compare only characteristics both sides actually state. A chariot
            # is split across several profile rows -- the catalogue's Boar
            # Chariot carries T and W, the wiki's carries M/WS/S/I/A -- so a
            # blank on either side is a structural difference in how the model
            # is broken up, not a disagreement about a number.
            # BattleScribe writes a literal "-" for a characteristic that does
            # not apply, so "absent" is a dash, not an empty element.
            blank = {"", "-", "--", "n/a"}
            diff = []
            for k in STAT_ORDER:
                have = (pr["chars"].get(k) or "").strip()
                want = str(stats.get(k, "")).strip()
                if have.lower() in blank or want.lower() in blank:
                    continue
                if have != want:
                    diff.append((k, have, want))
            if diff:
                stat_rows.append((path.name, pr["name"], pr["line"], diff, wpath))

    cost_rows.sort(key=lambda r: -r[5])
    stat_rows.sort(key=lambda r: (-len(r[3]), r[0]))

    lines = [
        "# Numeric discrepancies against the wiki", "",
        "Generated by `wiki_xref.py --numbers` from wiki build `{}` (indexed {}).".format(
            wiki.build_id, wiki.generated_at), "",
        "**Nothing here has been changed.** These are for a human to adjudicate: "
        "either side may be the one that is wrong.", "",
        "## Scope limit", "",
        "The wiki carries points costs for magic items **only**. It has no cost for "
        "any unit, mount, weapon or upgrade, so those cannot be checked against this "
        "source at all. It also lost the profile table on 84 of its 88 weapon pages "
        "(the wiki embedded them as chart entries with no page of their own), and its "
        "army-list pages are structural - no points, no min/max, no equipment options.",
        "",
        "## Read the costs table with care", "",
        "An item listed several times at different costs is usually not a bug. The "
        "Bretonnian Virtues are priced per character rank, so the catalogue carries "
        "one entry per rank while the wiki records a single figure. Check whether a "
        "row is one of a set before treating it as wrong.", "",
        "Statline rows compare only characteristics both sides state. A blank on "
        "either side means the model is split into profile rows differently (chariots "
        "especially), which is a modelling difference, not a disagreement.", "",
        "## Magic item points costs ({} differences)".format(len(cost_rows)), "",
    ]
    if cost_rows:
        lines += ["| Item | Where | Catalogue | Wiki | Diff |",
                  "| --- | --- | ---: | ---: | ---: |"]
        for f, name, line, have, want, d, wpath in cost_rows:
            lines.append("| [{}]({}) | {}:{} | {:g} | {:g} | {:+g} |".format(
                name, "https://6th.whfb.app" + wpath, f, line, have, want, want - have))
    else:
        lines.append("None.")

    lines += ["", "## Unit statlines ({} models differ)".format(len(stat_rows)), ""]
    if stat_rows:
        lines += ["| Model | Where | Characteristic | Catalogue | Wiki |",
                  "| --- | --- | --- | ---: | ---: |"]
        for f, name, line, diff, wpath in stat_rows:
            for k, have, want in diff:
                lines.append("| [{}]({}) | {}:{} | {} | {} | {} |".format(
                    name, "https://6th.whfb.app" + wpath, f, line, k, have, want))
    else:
        lines.append("None.")
    lines.append("")

    out = out_dir / "numeric-discrepancies.md"
    out.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")
    print("wrote {} - {} cost differences, {} models with stat differences".format(
        out.name, len(cost_rows), len(stat_rows)))
    return 0


def write_stubs(out_dir, files, wiki):
    """Phase G: every rule still without a description, and why it was left."""
    rows = []
    for path in files:
        inv = cat_inventory(path)
        assocs = ARMY_ASSOC.get(path.name, [])
        described = {normalise(r["name"]) for r in inv["rules"] if r["desc"]}
        for r in inv["rules"]:
            if r["desc"]:
                continue
            c = classify(r["name"], wiki, assocs)
            key = normalise(r["name"])
            if c["bucket"] == "D":
                reason = "mechanical-tag"
            elif key in described:
                reason = "shared-rule"
            elif c["bucket"] == "E":
                reason = "no-coverage"
            elif c["hits"] and "Main Rulebook" in wiki.assoc(c["hits"][0]["path"]):
                reason = "core-rule"
            else:
                reason = "deferred"
            cov = c["hits"][0]["path"] if c["hits"] else "none"
            rows.append((path.name, r, reason, cov, c))

    order = {"no-coverage": 0, "deferred": 1, "core-rule": 2,
             "shared-rule": 3, "mechanical-tag": 4}
    rows.sort(key=lambda t: (order.get(t[2], 9), t[3] == "none", t[0], t[1]["line"]))

    lines = ["# Rules left undescribed", "",
             "Wiki build `{}`.".format(wiki.build_id), "",
             "Sorted so the rows worth a human's time come first. A "
             "`mechanical-tag` row with no wiki coverage is self-evidently fine.", "",
             "| Rule | id | Where | Reason | Wiki coverage |",
             "| --- | --- | --- | --- | --- |"]
    flags, choices = [], []
    for fname, r, reason, cov, c in rows:
        alts = [h["path"] for h in c.get("hits", [])]
        lines.append("| {} | `{}` | {}:{} | `{}` | {} |".format(
            r["name"], r["id"], fname, r["line"], reason,
            cov if len(alts) < 2 else "{} (+{} more)".format(cov, len(alts) - 1)))
        if len(alts) > 1:
            choices.append((r["name"], fname, r["line"], alts))
    if choices:
        lines += ["", "## Undecided: the wiki has more than one page for the name", "",
                  "The catalogue holds one rule element where the wiki splits the name "
                  "across several pages whose text genuinely differs. Picking one is a "
                  "modelling decision about what that element is for, not a lookup.", ""]
        for name, fname, line, alts in choices:
            lines.append("- **{}** ({}:{})".format(name, fname, line))
            for a in alts:
                lines.append("  - `{}`".format(a))
        if reason in ("mechanical-tag", "core-rule") and cov != "none":
            flags.append("- **{}** ({}:{}) is `{}` but the wiki *does* cover it at "
                         "`{}` - text was available and not used.".format(
                             r["name"], fname, r["line"], reason, cov))
    if flags:
        lines += ["", "## Flagged: text was available and deliberately not used", ""] + flags
    lines.append("")
    (out_dir / "left-undescribed.md").write_text("\n".join(lines) + "\n",
                                                 encoding="utf-8", newline="\n")
    print("wrote left-undescribed.md - {} rows, {} flagged".format(len(rows), len(flags)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
