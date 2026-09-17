#!/usr/bin/env python3
"""Look up BattleScribe ids by name, or names by id, across the repo.

Faster and more precise than grepping, because it reports what kind of element
each hit is and where it sits, which is what you need before writing a
targetId, childId or `field` reference.

Usage:
    python find_id.py Fear                      # every element whose name matches
    python find_id.py "Sword of" --tag selectionEntry
    python find_id.py 87db-2d4c-3fa6-6a26       # reverse lookup by id
    python find_id.py --in Dwarfs.cat Hammerers
    python find_id.py --dump-gst-reference      # regenerate the ID reference table
"""

from __future__ import annotations

import argparse
import re
import xml.etree.ElementTree as ET

from bsdata import ID_RE, repo_root, source_files, strip_ns

# Sections of the .gst worth listing in the reference table, in document order.
REFERENCE_SECTIONS = [
    ("publications", "publication", "Publications"),
    ("costTypes", "costType", "Cost types"),
    ("profileTypes", "profileType", "Profile types"),
    ("categoryEntries", "categoryEntry", "Categories"),
    ("forceEntries", "forceEntry", "Force entries"),
    ("sharedSelectionEntries", "selectionEntry", "Shared selection entries (common magic items, lores, roles)"),
    ("sharedSelectionEntryGroups", "selectionEntryGroup", "Shared selection entry groups"),
    ("sharedRules", "rule", "Shared rules"),
    ("sharedInfoGroups", "infoGroup", "Shared info groups"),
]


def walk(root):
    parents = {c: p for p in root.iter() for c in p}

    def trail(el):
        names, cur = [], el
        while cur is not None:
            nm = cur.get("name")
            if nm and strip_ns(cur.tag) not in ("characteristic",):
                names.append(nm)
            cur = parents.get(cur)
        return " < ".join(names[1:4])

    return trail


def search(root_dir, query, tag_filter, file_filter):
    by_id = ID_RE.match(query) is not None
    needle = query.lower()
    hits = []
    for path in source_files(root_dir):
        if file_filter and path.name != file_filter:
            continue
        text = path.read_text(encoding="utf-8")
        lines = {}
        for m in re.finditer(r'\sid="([^"]+)"', text):
            lines.setdefault(m.group(1), text.count("\n", 0, m.start()) + 1)
        tree = ET.parse(path)
        trail = walk(tree.getroot())
        for el in tree.getroot().iter():
            tag = strip_ns(el.tag)
            eid, name = el.get("id"), el.get("name")
            if tag_filter and tag != tag_filter:
                continue
            if by_id:
                if eid != query and el.get("targetId") != query:
                    continue
            elif not name or needle not in name.lower():
                continue
            hits.append((path.name, lines.get(eid, 0), tag, eid, name, trail(el)))
    return hits


def dump_reference(root_dir) -> str:
    gst = next((p for p in source_files(root_dir) if p.suffix == ".gst"), None)
    if gst is None:
        return "no .gst found"
    tree = ET.parse(gst)
    root = tree.getroot()
    ns = root.tag.split("}")[0] + "}"
    out = [
        "# Game system reference IDs",
        "",
        f"Generated from `{gst.name}` (revision "
        f"{root.get('revision')}) by `scripts/find_id.py --dump-gst-reference`.",
        "Re-run that after editing the .gst so this file does not go stale.",
        "",
        f"Game system id: `{root.get('id')}` — every catalogue carries this as "
        "`gameSystemId`.",
        "",
    ]
    for container, child, title in REFERENCE_SECTIONS:
        holder = root.find(ns + container)
        if holder is None:
            continue
        out.append(f"## {title}")
        out.append("")
        if child == "profileType":
            for pt in holder:
                out.append(f"`{pt.get('id')}` — profile type **{pt.get('name')}**")
                out.append("")
                out.append("| Characteristic | typeId |")
                out.append("| --- | --- |")
                for ct in pt.iter(ns + "characteristicType"):
                    out.append(f"| {ct.get('name')} | `{ct.get('id')}` |")
                out.append("")
            continue
        out.append("| Name | id |" + (" Notes |" if child in ("categoryEntry", "selectionEntry") else ""))
        out.append("| --- | --- |" + (" --- |" if child in ("categoryEntry", "selectionEntry") else ""))
        for el in holder:
            note = ""
            if child == "categoryEntry":
                note = " hidden |" if el.get("hidden") == "true" else "  |"
            elif child == "selectionEntry":
                cost = el.find(ns + "costs/" + ns + "cost")
                note = f" {int(float(cost.get('value')))} pts |" if cost is not None else "  |"
            out.append(f"| {el.get('name')} | `{el.get('id')}` |{note}")
        out.append("")
    return "\n".join(out)


def main() -> int:
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    ap.add_argument("query", nargs="?", help="name substring (case-insensitive) or an id")
    ap.add_argument("--tag", help="only this element kind, e.g. selectionEntry, rule, categoryEntry")
    ap.add_argument("--in", dest="file", help="only this data file, e.g. Dwarfs.cat")
    ap.add_argument("--root", help="repo root (default: auto-detected)")
    ap.add_argument("--dump-gst-reference", action="store_true",
                    help="print the game system ID reference table as markdown")
    args = ap.parse_args()

    root_dir = repo_root(args.root)

    if args.dump_gst_reference:
        print(dump_reference(root_dir))
        return 0

    if not args.query:
        ap.error("give a query, or --dump-gst-reference")

    hits = search(root_dir, args.query, args.tag, args.file)
    if not hits:
        print(f"no match for {args.query!r}")
        return 1
    for name, line, tag, eid, label, trail in hits:
        loc = f"{name}:{line}" if line else name
        print(f"{loc:34s} <{tag}> {eid or '-'}  {label}" + (f"   [{trail}]" if trail else ""))
    print(f"\n{len(hits)} match(es)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
