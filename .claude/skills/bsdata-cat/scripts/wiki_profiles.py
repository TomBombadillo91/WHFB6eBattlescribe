#!/usr/bin/env python3
"""Give profile-less model entries their statline from the scraped wiki.

Companion to wiki_xref.py / wiki_apply.py, and the same text surgery: only the
targeted byte span is rewritten, CRLF and BattleScribe's escaping are preserved,
and nothing is round-tripped through an XML serialiser.

Only entries the wiki states a full statline for are touched. Crew, mounts and
components the wiki does not break out separately are left alone.

Usage:
    python wiki_profiles.py                     # dry run, all catalogues
    python wiki_profiles.py --only "Dwarfs.cat" --write
"""

from __future__ import annotations

import argparse
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

from bsdata import CAT_NS, repo_root, source_files
from new_id import mint, used_ids
from wiki_xref import Wiki, find_wiki, _best, STAT_ORDER, xml_escape
from wiki_apply import (element_span, read_exact, write_exact, bump_revision,
                        insertion_point)

MODEL_TYPE_ID = "0a0f-00cd-0261-c0ea"

# characteristicType ids from the .gst profileType "Model"
CHAR_IDS = {
    "M": "da3c-fb2b-4c5f-a22b", "WS": "d46f-1ae5-387f-4ac3",
    "BS": "22c7-799b-e07c-f32c", "S": "0c58-1252-962d-8fcc",
    "T": "16d7-9f22-06d8-8427", "W": "f9d0-a5b0-7e0b-a404",
    "I": "b418-0e30-644f-1435", "A": "fa03-f9a3-8117-98dd",
    "Ld": "bbad-d421-400b-87c1",
}


def profile_block(indent, pid, name, stats):
    nl = "\r\n"
    out = ['{}<profile id="{}" name="{}" hidden="false" typeId="{}" typeName="Model">'.format(
        indent, pid, xml_escape(name), MODEL_TYPE_ID)]
    out.append("{}  <characteristics>".format(indent))
    for k in STAT_ORDER:
        out.append('{}    <characteristic name="{}" typeId="{}">{}</characteristic>'.format(
            indent, k, CHAR_IDS[k], xml_escape(str(stats.get(k, "-")).strip() or "-")))
    out.append("{}  </characteristics>".format(indent))
    out.append("{}</profile>".format(indent))
    return nl.join(out)


def targets(path, wiki):
    """Profile-less model entries the wiki states a full statline for."""
    ns = "{%s}" % CAT_NS
    root = ET.fromstring(read_exact(path))
    found = []
    for se in root.iter(ns + "selectionEntry"):
        if se.get("type") != "model":
            continue
        pr = se.find(ns + "profiles")
        if pr is not None and len(pr):
            continue
        name = se.get("name") or ""
        wpath = _best(wiki, name, "unit")
        if not wpath:
            continue
        stats = (wiki.pages.get(wpath) or {}).get("statistics") or {}
        # Require the whole statline. A partial one means the wiki splits the
        # model across rows (chariots), which is not a gap this can fill.
        if not all(str(stats.get(k, "")).strip() for k in STAT_ORDER):
            continue
        found.append({"name": name, "id": se.get("id") or "",
                      "stats": stats, "wiki": wpath})
    return found


def insert(text, row, pid):
    """<profiles> goes after </constraints> and before <rules>/<categoryLinks>."""
    span = element_span(text, row["id"])
    if not span:
        return text, "id not found"
    start, end, _tag, indent, self_closing = span
    if self_closing:
        return text, "entry is self-closing"
    src = text[start:end]
    inner = indent + "  "
    block = "\r\n{i}<profiles>\r\n{p}\r\n{i}</profiles>".format(
        i=inner, p=profile_block(inner + "  ", pid, row["name"], row["stats"]))

    cut = insertion_point(
        src,
        after=("constraints", "modifierGroups", "modifiers"),
        before=("rules", "infoGroups", "infoLinks", "categoryLinks",
                "selectionEntries", "selectionEntryGroups", "entryLinks", "costs"),
    )
    if cut is None:
        return text, "no insertion point"
    if src[cut - 1] == ">":
        return text[:start] + src[:cut] + block + src[cut:] + text[end:], "inserted"
    return (text[:start] + src[:cut].rstrip("\r\n") + block + "\r\n"
            + src[cut:] + text[end:], "inserted")


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--wiki")
    ap.add_argument("--only")
    ap.add_argument("--write", action="store_true")
    ap.add_argument("--root")
    args = ap.parse_args()

    root = repo_root(args.root)
    wiki = Wiki(find_wiki(args.wiki))
    files = [p for p in source_files(root)
             if p.suffix == ".cat" and (not args.only or p.name == args.only)]

    for path in files:
        rows = targets(path, wiki)
        if not rows:
            continue
        text = read_exact(path)
        taken = used_ids(root)
        ids = []
        for _ in rows:
            fresh = mint(taken)
            taken.add(fresh)
            ids.append(fresh)

        bad = []
        # Back to front: each insert shifts every offset after it.
        order = sorted(range(len(rows)), key=lambda i: text.find(rows[i]["id"]), reverse=True)
        for i in order:
            text, what = insert(text, rows[i], ids[i])
            if what != "inserted":
                bad.append((rows[i]["name"], what))
        text, rev = bump_revision(text)
        print("{}: {} profiles, revision -> {}{}".format(
            path.name, len(rows) - len(bad), rev,
            "  [{} FAILED]".format(len(bad)) if bad else ""))
        for n, w in bad:
            print("   !! {}: {}".format(n, w))
        if args.write:
            write_exact(path, text)
        else:
            print("   (dry run - pass --write to apply)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
