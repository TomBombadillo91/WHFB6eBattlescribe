#!/usr/bin/env python3
"""Put core rulebook rules in the game system once, and link to them.

Mundane weapons, musicians, champions and wizard levels are core rules that
every army uses. Giving each catalogue its own copy would mean 379 duplicate
descriptions that drift apart; they belong in the .gst's <sharedRules>, with
each catalogue carrying an <infoLink> to the one definition.

Long rules are skipped. A page over MAX_CHARS is a rulebook chapter rather
than a rule -- Skirmishers is 4318 characters and Cannons 3650 -- and those
stay as named stubs, which is how the .gst already treats them.

Usage:
    python wiki_core.py                  # dry run
    python wiki_core.py --write
"""

from __future__ import annotations

import argparse
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

from bsdata import CAT_NS, GST_NS, repo_root, source_files
from new_id import mint, used_ids
from wiki_xref import (Wiki, find_wiki, classify, normalise, wiki_rules_text,
                       xml_escape, ARMY_ASSOC, variants)
from wiki_apply import (element_span, read_exact, write_exact, bump_revision,
                        insertion_point, rule_block)

MAX_CHARS = 1500

# Core pages worth carrying that no catalogue entry points at by name.
EXTRA = ("/war-machines/bolt-throwers",)


def core_targets(root, wiki):
    """{wiki path: [(file, entry id, entry name)]} for textless core entries."""
    ns = "{%s}" % CAT_NS
    out = {}
    for path in source_files(root):
        if path.suffix != ".cat":
            continue
        tree = ET.fromstring(read_exact(path))
        for se in tree.iter(ns + "selectionEntry"):
            if se.get("type") != "upgrade":
                continue
            if any(se.find(ns + x) is not None and len(se.find(ns + x))
                   for x in ("rules", "profiles", "infoLinks")):
                continue
            c = classify(se.get("name") or "", wiki, ARMY_ASSOC.get(path.name, []))
            if c["bucket"] not in ("A", "B") or not c["hits"]:
                continue
            wpath = c["hits"][0]["path"]
            if "Main Rulebook" not in wiki.assoc(wpath):
                continue
            try:
                body, _ = wiki_rules_text(wiki.text(wpath))
            except (KeyError, OSError):
                continue
            if not body.strip() or len(body) > MAX_CHARS:
                continue
            out.setdefault(wpath, []).append((path.name, se.get("id"), se.get("name")))
    return out


def gst_rules(text):
    """{normalised name: (id, has description)} for the game system's rules."""
    ns = "{%s}" % GST_NS
    g = ET.fromstring(text)
    out = {}
    for ru in g.iter(ns + "rule"):
        d = ru.find(ns + "description")
        out[normalise(ru.get("name") or "")] = (
            ru.get("id"), bool(d is not None and (d.text or "").strip()))
    return out


def add_shared(text, name, body, rid):
    """Append a described rule to the game system's <sharedRules>."""
    m = re.search(r"([ \t]*)</sharedRules>", text)
    if not m:
        return text, None
    indent = m.group(1) + "  "
    block = rule_block(indent, rid, name, body) + "\r\n"
    return text[:m.start()] + block + text[m.start():], rid


def fill_stub(text, rid, name, body):
    span = element_span(text, rid)
    if not span:
        return text, False
    start, end, _t, indent, _sc = span
    src = text[start:end]
    if "<description>" in src:
        return text, False
    new = rule_block(indent, rid, name, body)[len(indent):]
    return text[:start] + new + text[end:], True


def add_infolink(text, entry_id, name, target, link_id):
    """Give a textless entry an <infoLinks> block pointing at the shared rule."""
    span = element_span(text, entry_id)
    if not span:
        return text, "id not found"
    start, end, _t, indent, self_closing = span
    if self_closing:
        return text, "entry is self-closing"
    src = text[start:end]
    inner = indent + "  "
    block = ('\r\n{i}<infoLinks>\r\n{i}  <infoLink id="{l}" name="{n}" hidden="false"'
             ' targetId="{t}" type="rule"/>\r\n{i}</infoLinks>').format(
        i=inner, l=link_id, n=xml_escape(name), t=target)
    cut = insertion_point(
        src,
        after=("infoGroups", "rules", "profiles", "constraints",
               "modifierGroups", "modifiers"),
        before=("categoryLinks", "selectionEntries", "selectionEntryGroups",
                "entryLinks", "costs"),
    )
    if cut is None:
        return text, "no insertion point"
    if src[cut - 1] == ">":
        return text[:start] + src[:cut] + block + src[cut:] + text[end:], "linked"
    return (text[:start] + src[:cut].rstrip("\r\n") + block + "\r\n"
            + src[cut:] + text[end:], "linked")


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--wiki")
    ap.add_argument("--write", action="store_true")
    ap.add_argument("--root")
    args = ap.parse_args()

    root = repo_root(args.root)
    wiki = Wiki(find_wiki(args.wiki))
    gst = next(p for p in source_files(root) if p.suffix == ".gst")

    targets = core_targets(root, wiki)
    for extra in EXTRA:
        targets.setdefault(extra, [])

    taken = used_ids(root)

    def fresh():
        i = mint(taken)
        taken.add(i)
        return i

    # ---------------------------------------------------- game system
    gtext = read_exact(gst)
    existing = gst_rules(gtext)
    target_id, added, filled = {}, 0, 0
    for wpath in sorted(targets):
        name = wiki.pages[wpath]["name"]
        body, _ = wiki_rules_text(wiki.text(wpath))
        if len(body) > MAX_CHARS or not body.strip():
            continue
        # Match the .gst's own spelling too. Its stub is "Bolt Thrower" where
        # the wiki page is "Bolt Throwers"; adding a second rule would leave
        # the stub in place, still bare, with every existing infoLink pointing
        # at it - so fill the stub instead.
        key = next((k for k in [normalise(name)] + [normalise(v) for v in variants(name)]
                    if k in existing), normalise(name))
        if key in existing:
            rid, described = existing[key]
            target_id[wpath] = rid
            if not described:
                gtext, ok = fill_stub(gtext, rid, name, body)
                filled += ok
            continue
        rid = fresh()
        gtext, ok = add_shared(gtext, name, body, rid)
        if ok:
            target_id[wpath] = rid
            added += 1

    gtext, grev = bump_revision(gtext)
    print("{}: +{} shared rules, {} stubs filled, revision -> {}".format(
        gst.name, added, filled, grev))

    # ---------------------------------------------------- catalogues
    per_file = {}
    for wpath, uses in targets.items():
        if wpath not in target_id:
            continue
        for fname, eid, ename in uses:
            per_file.setdefault(fname, []).append((eid, ename, target_id[wpath]))

    total = 0
    for path in source_files(root):
        rows = per_file.get(path.name)
        if not rows:
            continue
        text = read_exact(path)
        bad = []
        # Back to front so earlier offsets stay valid.
        rows.sort(key=lambda r: text.find(r[0]), reverse=True)
        for eid, ename, tid in rows:
            text, what = add_infolink(text, eid, ename, tid, fresh())
            if what != "linked":
                bad.append((ename, what))
        text, rev = bump_revision(text)
        total += len(rows) - len(bad)
        print("{:34} {:4} infoLinks, revision -> {}{}".format(
            path.name, len(rows) - len(bad), rev,
            "  [{} FAILED]".format(len(bad)) if bad else ""))
        for n, wtxt in bad:
            print("   !! {}: {}".format(n, wtxt))
        if args.write:
            write_exact(path, text)

    print("\n{} entries linked to {} shared rules".format(total, len(target_id)))
    if args.write:
        write_exact(gst, gtext)
    else:
        print("(dry run - pass --write to apply)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
