#!/usr/bin/env python3
"""Structural validator for the WHFB6e BattleScribe data files.

Catches the mistakes BattleScribe itself only reports at load time (or, worse,
silently swallows): dangling targetId/childId references, malformed or
duplicated IDs, characteristics that do not match the game system's profile
type, elements written under a parent that cannot hold them, out-of-order
child elements, and Deploy/ drifting from the root files.

Usage:
    python validate.py                  # every .cat + the .gst
    python validate.py Dwarfs.cat       # one or more files
    python validate.py --no-deploy      # skip the Deploy/ consistency section
    python validate.py --root DIR
"""

from __future__ import annotations

import argparse
import re
import sys
import xml.etree.ElementTree as ET
import zipfile
from collections import defaultdict
from pathlib import Path

from bsdata import ID_RE, deploy_name, read_text, repo_root, root_attr, source_files, strip_ns

# ---------------------------------------------------------------- vocabularies

SCOPE_KEYWORDS = {"self", "parent", "force", "roster", "primary-catalogue", "ancestor"}
CHILD_KEYWORDS = {"model", "unit", "upgrade"}
FIELD_KEYWORDS = {
    "selections",
    "forces",
    "hidden",
    "name",
    "description",
    "category",
    "page",
    "import",
}
MODIFIER_TYPES = {
    "set",
    "increment",
    "decrement",
    "append",
    "add",
    "remove",
    "set-primary",
    "unset-primary",
}
CONDITION_TYPES = {
    "equalTo",
    "notEqualTo",
    "atLeast",
    "atMost",
    "greaterThan",
    "lessThan",
    "instanceOf",
    "notInstanceOf",
}
CONSTRAINT_TYPES = {"min", "max"}

LINK_TARGET_KINDS = {
    ("entryLink", "selectionEntry"): {"selectionEntry"},
    ("entryLink", "selectionEntryGroup"): {"selectionEntryGroup"},
    ("infoLink", "rule"): {"rule"},
    ("infoLink", "profile"): {"profile"},
    ("infoLink", "infoGroup"): {"infoGroup"},
    ("categoryLink", None): {"categoryEntry"},
    ("catalogueLink", "catalogue"): {"catalogue", "gameSystem"},
}

# Canonical child ordering, as written by BattleScribe 2.03.
CHILD_ORDER = {
    "gameSystem": [
        "readme", "publications", "costTypes", "profileTypes", "categoryEntries",
        "forceEntries", "selectionEntries", "entryLinks", "rules",
        "sharedSelectionEntries", "sharedSelectionEntryGroups", "sharedRules",
        "sharedProfiles", "sharedInfoGroups",
    ],
    "catalogue": [
        "readme", "publications", "costTypes", "categoryEntries", "selectionEntries",
        "entryLinks", "rules", "infoLinks", "sharedSelectionEntries",
        "sharedSelectionEntryGroups", "sharedRules", "sharedProfiles",
        "sharedInfoGroups", "catalogueLinks",
    ],
    "selectionEntry": [
        "modifiers", "modifierGroups", "constraints", "profiles", "rules",
        "infoGroups", "infoLinks", "categoryLinks", "selectionEntries",
        "selectionEntryGroups", "entryLinks", "costs",
    ],
    "selectionEntryGroup": [
        "modifiers", "modifierGroups", "constraints", "profiles", "rules",
        "infoGroups", "infoLinks", "categoryLinks", "selectionEntries",
        "selectionEntryGroups", "entryLinks",
    ],
    "entryLink": [
        "modifiers", "modifierGroups", "constraints", "profiles", "rules",
        "infoGroups", "infoLinks", "categoryLinks", "costs",
    ],
    "categoryEntry": ["modifiers", "modifierGroups", "constraints", "profiles",
                      "rules", "infoGroups", "infoLinks"],
    "categoryLink": ["modifiers", "modifierGroups", "constraints"],
    "profile": ["modifiers", "modifierGroups", "characteristics"],
    "rule": ["modifiers", "modifierGroups", "description"],
    "infoGroup": ["modifiers", "modifierGroups", "profiles", "rules", "infoLinks"],
    "infoLink": ["modifiers", "modifierGroups"],
    "modifier": ["repeats", "conditions", "conditionGroups"],
    "modifierGroup": ["comment", "repeats", "conditions", "conditionGroups", "modifiers",
                      "modifierGroups"],
    "conditionGroup": ["conditions", "conditionGroups"],
}


class Report:
    def __init__(self) -> None:
        self.errors: list[str] = []
        self.warnings: list[str] = []

    def error(self, msg: str) -> None:
        self.errors.append(msg)

    def warn(self, msg: str) -> None:
        self.warnings.append(msg)


class DataFile:
    """One parsed .cat/.gst plus the indexes the checks need."""

    def __init__(self, path: Path) -> None:
        self.path = path
        self.name = path.name
        self.text = read_text(path)
        self.tree = ET.parse(path)
        self.root = self.tree.getroot()
        self.kind = strip_ns(self.root.tag)  # catalogue | gameSystem
        self.id = self.root.get("id")
        self.parents: dict[ET.Element, ET.Element] = {}
        self.line_of: dict[str, int] = {}
        self.ids: dict[str, ET.Element] = {}
        for parent in self.root.iter():
            for child in parent:
                self.parents[child] = parent
        for el in self.root.iter():
            eid = el.get("id")
            if eid and eid not in self.ids:
                self.ids[eid] = el
        for m in re.finditer(r'\sid="([^"]+)"', self.text):
            self.line_of.setdefault(m.group(1), self.text.count("\n", 0, m.start()) + 1)
        if self.id:
            self.ids.setdefault(self.id, self.root)
            self.line_of.setdefault(self.id, 2)

    def where(self, el: ET.Element) -> str:
        """`file:line` for the nearest enclosing element that carries an id."""
        cur: ET.Element | None = el
        while cur is not None:
            eid = cur.get("id")
            if eid and eid in self.line_of:
                return f"{self.name}:{self.line_of[eid]}"
            cur = self.parents.get(cur)
        return self.name

    def describe(self, el: ET.Element) -> str:
        cur: ET.Element | None = el
        trail = []
        while cur is not None and len(trail) < 3:
            nm = cur.get("name")
            if nm:
                trail.append(nm)
            cur = self.parents.get(cur)
        return " < ".join(trail) if trail else strip_ns(el.tag)


def load(root: Path) -> dict[str, DataFile]:
    files: dict[str, DataFile] = {}
    for path in source_files(root):
        files[path.name] = DataFile(path)
    return files


def linked_scope(df: DataFile, by_id: dict[str, DataFile], gst: DataFile | None) -> list[DataFile]:
    """The file itself, the game system, and every catalogue it links to."""
    scope = [df]
    if gst is not None and gst is not df:
        scope.append(gst)
    pending = [df]
    seen = {df.name}
    while pending:
        cur = pending.pop()
        for link in cur.root.iter():
            if strip_ns(link.tag) != "catalogueLink":
                continue
            target = by_id.get(link.get("targetId") or "")
            if target is not None and target.name not in seen:
                seen.add(target.name)
                scope.append(target)
                pending.append(target)
    return scope


# ------------------------------------------------------------------- checks


def check_ids(df: DataFile, rep: Report) -> None:
    counts: dict[str, int] = defaultdict(int)
    for m in re.finditer(r'\sid="([^"]+)"', df.text):
        counts[m.group(1)] += 1
        if not ID_RE.match(m.group(1)):
            line = df.text.count("\n", 0, m.start()) + 1
            rep.error(f"{df.name}:{line}: malformed id {m.group(1)!r} "
                      f"(expected four lowercase hex quads, e.g. 1a2b-3c4d-5e6f-7a8b)")
    for eid, n in counts.items():
        if n > 1:
            rep.error(f"{df.name}:{df.line_of.get(eid, 0)}: id {eid} used {n} times in this file")


def check_references(df: DataFile, scope: list[DataFile], catalogue_ids: set[str],
                     rep: Report) -> None:
    known: dict[str, str] = {}
    for other in scope:
        for eid, el in other.ids.items():
            known.setdefault(eid, strip_ns(el.tag))
    scope_names = ", ".join(s.name for s in scope)

    for el in df.root.iter():
        tag = strip_ns(el.tag)

        target = el.get("targetId")
        if target is not None:
            expect = LINK_TARGET_KINDS.get((tag, el.get("type")))
            if expect is None:
                expect = LINK_TARGET_KINDS.get((tag, None))
            actual = known.get(target)
            if actual is None:
                rep.error(f"{df.where(el)}: {tag} {el.get('name')!r} targets missing id "
                          f"{target} (searched {scope_names})")
            elif expect and actual not in expect:
                rep.error(f"{df.where(el)}: {tag} {el.get('name')!r} has type="
                          f"{el.get('type')!r} but {target} is a <{actual}>")

        child = el.get("childId")
        if child is not None and child not in CHILD_KEYWORDS and child not in known:
            # scope="primary-catalogue" tests the roster's army book, so childId is a
            # catalogue id from anywhere in the repo rather than a linked entry.
            if not (el.get("scope") == "primary-catalogue" and child in catalogue_ids):
                rep.error(f"{df.where(el)}: <{tag}> childId={child} does not resolve "
                          f"({df.describe(el)})")

        scope_attr = el.get("scope")
        if scope_attr is not None and scope_attr not in SCOPE_KEYWORDS and scope_attr not in known:
            rep.error(f"{df.where(el)}: <{tag}> scope={scope_attr!r} is neither a keyword "
                      f"({'/'.join(sorted(SCOPE_KEYWORDS))}) nor a known id")

        field = el.get("field")
        if field is not None:
            bare = field[len("limit::"):] if field.startswith("limit::") else field
            if bare not in FIELD_KEYWORDS and bare not in known:
                rep.error(f"{df.where(el)}: <{tag}> field={field!r} is neither a keyword "
                          f"nor a known id ({df.describe(el)})")

        if tag == "modifier" and el.get("type") not in MODIFIER_TYPES:
            rep.error(f"{df.where(el)}: modifier type={el.get('type')!r} unknown")
        if tag == "condition" and el.get("type") not in CONDITION_TYPES:
            rep.error(f"{df.where(el)}: condition type={el.get('type')!r} unknown")
        if tag == "constraint" and el.get("type") not in CONSTRAINT_TYPES:
            rep.error(f"{df.where(el)}: constraint type={el.get('type')!r} unknown "
                      f"(expected min or max)")

        if tag == "categoryLinks":
            primary = [c for c in el if c.get("primary") == "true"]
            if len(primary) > 1:
                rep.error(f"{df.where(el)}: {len(primary)} categoryLinks marked primary "
                          f"({', '.join(c.get('name') or '?' for c in primary)}); "
                          f"exactly one should be")

        if tag == "selectionEntryGroup":
            default = el.get("defaultSelectionEntryId")
            if default:
                options = set()
                for holder in el:
                    if strip_ns(holder.tag) in ("selectionEntries", "entryLinks"):
                        options.update(c.get("id") for c in holder)
                        options.update(c.get("targetId") for c in holder)
                if default not in options:
                    rep.error(f"{df.where(el)}: group {el.get('name')!r} has "
                              f"defaultSelectionEntryId={default}, which is not one of "
                              f"its own options")


def check_profiles(df: DataFile, gst: DataFile | None, rep: Report) -> None:
    if gst is None:
        return
    types: dict[str, tuple[str, dict[str, str]]] = {}
    for pt in gst.root.iter():
        if strip_ns(pt.tag) != "profileType":
            continue
        chars = {c.get("id"): c.get("name") for c in pt.iter() if strip_ns(c.tag) == "characteristicType"}
        types[pt.get("id")] = (pt.get("name"), chars)

    costs = {c.get("id"): c.get("name") for c in gst.root.iter() if strip_ns(c.tag) == "costType"}
    costs.update({c.get("id"): c.get("name") for c in df.root.iter() if strip_ns(c.tag) == "costType"})

    for el in df.root.iter():
        tag = strip_ns(el.tag)
        if tag == "profile":
            info = types.get(el.get("typeId"))
            if info is None:
                rep.error(f"{df.where(el)}: profile {el.get('name')!r} has unknown "
                          f"typeId={el.get('typeId')}")
                continue
            type_name, chars = info
            if el.get("typeName") != type_name:
                rep.error(f"{df.where(el)}: profile {el.get('name')!r} has typeName="
                          f"{el.get('typeName')!r}, expected {type_name!r}")
            present = []
            for ch in el.iter():
                if strip_ns(ch.tag) != "characteristic":
                    continue
                expected = chars.get(ch.get("typeId"))
                if expected is None:
                    rep.error(f"{df.where(el)}: profile {el.get('name')!r} has "
                              f"characteristic {ch.get('name')!r} with unknown typeId")
                    continue
                if ch.get("name") != expected:
                    rep.error(f"{df.where(el)}: profile {el.get('name')!r} characteristic "
                              f"typeId {ch.get('typeId')} is named {ch.get('name')!r}, "
                              f"expected {expected!r}")
                present.append(ch.get("typeId"))
            missing = [chars[k] for k in chars if k not in present]
            if missing:
                rep.warn(f"{df.where(el)}: profile {el.get('name')!r} is missing "
                         f"characteristics: {', '.join(missing)}")
            if present != [k for k in chars if k in present]:
                rep.warn(f"{df.where(el)}: profile {el.get('name')!r} lists characteristics "
                         f"out of the game system's order")
        elif tag == "cost":
            expected = costs.get(el.get("typeId"))
            if expected is None:
                rep.error(f"{df.where(el)}: cost has unknown typeId={el.get('typeId')}")
            elif el.get("name") != expected:
                rep.error(f"{df.where(el)}: cost typeId {el.get('typeId')} is named "
                          f"{el.get('name')!r}, expected {expected!r}")


def container_for(ctag: str) -> str:
    """The wrapper a stray child almost always belongs in: rule -> rules."""
    return ctag[:-1] + "ies" if ctag.endswith("y") else ctag + "s"


def check_parentage(df: DataFile, rep: Report) -> None:
    """Reject a child element its parent has no slot for.

    Out-of-order children are cosmetic -- BattleScribe rewrites them on save --
    but a child under the wrong parent is invalid, and check_order used to skip
    silently over exactly that case. A <rule> written straight into a
    <selectionEntry> instead of into its <rules> container validated clean and
    was only caught by reading the diff.
    """
    for parent in df.root.iter():
        ptag = strip_ns(parent.tag)
        order = CHILD_ORDER.get(ptag)
        if not order:
            continue
        for child in parent:
            ctag = strip_ns(child.tag)
            if ctag in order:
                continue
            hint = container_for(ctag)
            fix = f"; it belongs in <{hint}>" if hint in order else ""
            rep.error(f"{df.where(child)}: <{ptag}> cannot contain <{ctag}>{fix}. "
                      f"BattleScribe allows {' > '.join(order)}")


def check_order(df: DataFile, rep: Report) -> None:
    for parent in df.root.iter():
        ptag = strip_ns(parent.tag)
        order = CHILD_ORDER.get(ptag)
        if not order:
            continue
        rank = {name: i for i, name in enumerate(order)}
        last = -1
        last_name = ""
        for child in parent:
            ctag = strip_ns(child.tag)
            if ctag not in rank:
                continue
            if rank[ctag] < last:
                rep.warn(f"{df.where(parent)}: <{ptag}> has <{ctag}> after <{last_name}>; "
                         f"BattleScribe writes {' > '.join(order)}")
                break
            last, last_name = rank[ctag], ctag


def check_header(df: DataFile, gst: DataFile | None, rep: Report) -> None:
    if df.kind != "catalogue" or gst is None:
        return
    if df.root.get("gameSystemId") != gst.id:
        rep.error(f"{df.name}:2: gameSystemId={df.root.get('gameSystemId')} does not match "
                  f"{gst.name} ({gst.id})")
    if df.root.get("name") != df.path.stem:
        rep.warn(f"{df.name}:2: catalogue name {df.root.get('name')!r} does not match the "
                 f"filename; BattleScribe names the archive after the catalogue")


def check_cross_file_ids(files: dict[str, DataFile], by_id: dict[str, DataFile],
                         gst: DataFile | None, rep: Report) -> None:
    owners: dict[str, list[DataFile]] = defaultdict(list)
    for df in files.values():
        for eid in df.ids:
            owners[eid].append(df)
    for eid, holders in owners.items():
        if len(holders) < 2:
            continue
        names = ", ".join(h.name for h in holders)
        clash = False
        for df in holders:
            scope = {s.name for s in linked_scope(df, by_id, gst)}
            if any(o.name in scope for o in holders if o is not df):
                clash = True
        if clash:
            rep.error(f"id {eid} is defined in {names}, which are loaded together "
                      f"(catalogueLink); ids must be unique across a loaded roster")
        else:
            rep.warn(f"id {eid} is defined in {names} (copy/paste without re-minting ids); "
                     f"harmless only while those catalogues are never loaded together")


def check_deploy(root: Path, files: dict[str, DataFile], rep: Report) -> None:
    deploy = root / "Deploy"
    index = deploy / "index.xml"
    if not index.exists():
        rep.warn("Deploy/index.xml is missing; run build_deploy.py")
        return
    idx = read_text(index)
    entries = {
        m.group(1): m.group(2)
        for m in re.finditer(r'filePath="([^"]+)"[^>]*dataRevision="(\d+)"', idx)
    }
    for df in files.values():
        archive_name = deploy_name(df.path)
        archive = deploy / archive_name
        revision = root_attr(df.text, "revision")
        if not archive.exists():
            rep.error(f"Deploy/{archive_name} is missing; run build_deploy.py")
            continue
        try:
            packed = zipfile.ZipFile(archive).read(df.name).decode("utf-8")
        except (KeyError, zipfile.BadZipFile) as exc:
            rep.error(f"Deploy/{archive_name} is not a readable archive holding {df.name}: {exc}")
            continue
        packed_rev = root_attr(packed, "revision")
        if packed_rev != revision:
            rep.error(f"{df.name} is revision {revision} but Deploy/{archive_name} holds "
                      f"revision {packed_rev}; run build_deploy.py")
        if entries.get(archive_name) != revision:
            rep.error(f"Deploy/index.xml lists {archive_name} at revision "
                      f"{entries.get(archive_name)}, file is {revision}; run build_deploy.py")
    for path in entries:
        if not any(deploy_name(df.path) == path for df in files.values()):
            rep.error(f"Deploy/index.xml lists {path}, which has no source file in the repo root")


# --------------------------------------------------------------------- main


def main() -> int:
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    ap.add_argument("files", nargs="*", help="specific .cat/.gst files (default: all)")
    ap.add_argument("--root", help="repo root (default: auto-detected)")
    ap.add_argument("--no-deploy", action="store_true", help="skip Deploy/ consistency checks")
    ap.add_argument("-q", "--quiet", action="store_true", help="errors only, no warnings")
    ap.add_argument("--max-warnings", type=int, metavar="N",
                    help="fail if more than N warnings (the accepted baseline is 159)")
    args = ap.parse_args()

    root = repo_root(args.root)
    rep = Report()

    try:
        files = load(root)
    except ET.ParseError as exc:
        print(f"XML is not well-formed: {exc}", file=sys.stderr)
        return 2

    gst = next((f for f in files.values() if f.kind == "gameSystem"), None)
    by_id = {f.id: f for f in files.values() if f.id}
    catalogue_ids = set(by_id)

    selected = list(files.values())
    if args.files:
        wanted = {Path(f).name for f in args.files}
        selected = [f for f in files.values() if f.name in wanted]
        missing = wanted - {f.name for f in selected}
        for name in sorted(missing):
            print(f"no such data file in {root}: {name}", file=sys.stderr)
        if missing:
            return 2

    for df in selected:
        check_ids(df, rep)
        check_references(df, linked_scope(df, by_id, gst), catalogue_ids, rep)
        check_profiles(df, gst, rep)
        check_parentage(df, rep)
        check_order(df, rep)
        check_header(df, gst, rep)

    if not args.files:
        check_cross_file_ids(files, by_id, gst, rep)
        if not args.no_deploy:
            check_deploy(root, files, rep)

    if not args.quiet:
        for msg in rep.warnings:
            print(f"warning: {msg}")
    for msg in rep.errors:
        print(f"error: {msg}")

    checked = ", ".join(sorted(f.name for f in selected)) if args.files else f"{len(selected)} files"
    print(f"\nchecked {checked}: {len(rep.errors)} error(s), {len(rep.warnings)} warning(s)")

    over_budget = args.max_warnings is not None and len(rep.warnings) > args.max_warnings
    if over_budget:
        print(f"error: {len(rep.warnings)} warnings exceeds the accepted baseline of "
              f"{args.max_warnings}; see 'Accepted validator warnings' in CLAUDE.md")
    return 1 if rep.errors or over_budget else 0


if __name__ == "__main__":
    raise SystemExit(main())
