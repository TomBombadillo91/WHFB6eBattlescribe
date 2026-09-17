#!/usr/bin/env python3
"""Apply wiki_xref.py's confident matches to a catalogue, as text surgery.

Companion to wiki_xref.py, which only ever reports. This writes, but it is still
*text* editing: it rewrites only the byte spans it targets and leaves the rest of
the file untouched, so the diff stays reviewable. Nothing is ever round-tripped
through an XML serialiser -- that would rewrite BattleScribe's &apos;/&quot;
escaping, self-closing tags and CRLF line endings across thousands of lines.

Only buckets A and B are applied. C, D and E are reported by wiki_xref.py and
resolved by hand.

Usage:
    python wiki_apply.py --only "Vampire Counts.cat"            # dry run
    python wiki_apply.py --only "Vampire Counts.cat" --write
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

from bsdata import repo_root, source_files
from new_id import mint, used_ids
from wiki_xref import Wiki, analyse, find_wiki, xml_escape


def read_exact(path):
    """Read preserving CRLF; the repo's data files are CRLF with no final newline."""
    return path.read_text(encoding="utf-8", newline="")


def write_exact(path, text):
    with path.open("w", encoding="utf-8", newline="") as fh:
        fh.write(text)


def element_span(text, eid):
    """Byte span of the element carrying this id, plus its tag and indentation."""
    m = re.search(r'<(\w+)([^>]*?\s)id="{}"'.format(re.escape(eid)), text)
    if not m:
        return None
    tag, start = m.group(1), m.start()
    line_start = text.rfind("\n", 0, start) + 1
    indent = text[line_start:start]
    # Walk to the end of the opening tag, respecting quoted attribute values.
    i, in_q = m.end(), None
    while i < len(text):
        ch = text[i]
        if in_q:
            in_q = None if ch == in_q else in_q
        elif ch in "\"'":
            in_q = ch
        elif ch == ">":
            break
        i += 1
    if text[i - 1] == "/":                      # self-closing
        return start, i + 1, tag, indent, True
    depth, j = 1, i + 1
    open_re = re.compile(r"<{0}\b|</{0}>".format(re.escape(tag)))
    while depth and j < len(text):
        mm = open_re.search(text, j)
        if not mm:
            return None
        if mm.group(0).startswith("</"):
            depth -= 1
            j = mm.end()
        else:
            # A self-closing nested tag of the same name never opens a level.
            k = text.index(">", mm.end())
            depth += 0 if text[k - 1] == "/" else 1
            j = k + 1
    return start, j, tag, indent, False


def rule_block(indent, rid, name, body):
    """A <rule> with a description, at BattleScribe's indentation and escaping."""
    nl = "\r\n"
    desc = xml_escape(body).replace("\n", nl)
    return (
        '{i}<rule id="{r}" name="{n}" hidden="false">{nl}'
        "{i}  <description>{d}</description>{nl}"
        "{i}</rule>"
    ).format(i=indent, r=rid, n=xml_escape(name), d=desc, nl=nl)


def apply_rule(text, row, _mint):
    """Give a <rule> the wiki's text, expanding a self-closing tag if need be."""
    span = element_span(text, row["id"])
    if not span:
        return text, "id not found"
    start, end, _tag, indent, _sc = span
    src = text[start:end]
    body = xml_escape(row["proposed"]).replace("\n", "\r\n")
    if "<description>" in src:
        new = re.sub(r"<description>.*?</description>",
                     lambda _: "<description>{}</description>".format(body),
                     src, count=1, flags=re.S)
        what = "replaced description"
    elif "<description/>" in src:
        new = src.replace("<description/>",
                          "<description>{}</description>".format(body), 1)
        what = "filled empty description"
    else:
        # start is the '<', so the leading indent is already in the text before
        # it; emit the block without its own first-line indent or the opening
        # tag lands twice-indented.
        new = rule_block(indent, row["id"], row["name"], row["proposed"])[len(indent):]
        what = "expanded stub"
    return text[:start] + new + text[end:], what


def apply_item(text, row, mint_id):
    """Insert a <rules> block into a magic-item entry that has no text at all.

    selectionEntry child order is modifiers, modifierGroups, constraints,
    profiles, rules, infoGroups, infoLinks, categoryLinks, selectionEntries,
    selectionEntryGroups, entryLinks, costs -- so <rules> goes after
    </constraints> (or </profiles>) and before <categoryLinks>.
    """
    span = element_span(text, row["id"])
    if not span:
        return text, "id not found"
    start, end, _tag, indent, self_closing = span
    if self_closing:
        return text, "entry is self-closing, needs manual handling"
    src = text[start:end]
    inner_indent = indent + "  "
    # The <rule> must sit inside a <rules> container -- a bare <rule> under a
    # selectionEntry is invalid, and validate.py does not currently catch it.
    block = ("\r\n{i}<rules>\r\n{r}\r\n{i}</rules>").format(
        i=inner_indent,
        r=rule_block(inner_indent + "  ", mint_id, row["name"], row["proposed"]),
    )

    for after in ("</profiles>", "</constraints>"):
        k = src.rfind(after)
        if k != -1:
            cut = k + len(after)
            return text[:start] + src[:cut] + block + src[cut:] + text[end:], "inserted rules block"
    for before in ("<infoGroups>", "<infoLinks>", "<categoryLinks>", "<selectionEntries>",
                   "<selectionEntryGroups>", "<entryLinks>", "<costs>"):
        k = src.find(before)
        if k != -1:
            line_start = src.rfind("\n", 0, k) + 1
            return (text[:start] + src[:line_start].rstrip("\r\n") + block + "\r\n"
                    + src[line_start:] + text[end:], "inserted rules block")
    return text, "no insertion point found"


def bump_revision(text):
    m = re.search(r'(<(?:catalogue|gameSystem)\b[^>]*?\srevision=")(\d+)(")', text)
    if not m:
        return text, None
    new = int(m.group(2)) + 1
    return text[:m.start()] + m.group(1) + str(new) + m.group(3) + text[m.end():], new


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--wiki")
    ap.add_argument("--only", help="one data file, e.g. 'Vampire Counts.cat'")
    ap.add_argument("--write", action="store_true", help="actually write (default: dry run)")
    ap.add_argument("--root")
    args = ap.parse_args()

    root = repo_root(args.root)
    wiki = Wiki(find_wiki(args.wiki))
    wiki.check_normalise()

    files = [p for p in source_files(root) if not args.only or p.name == args.only]
    if not files:
        sys.exit("no such data file: {}".format(args.only))

    for path in files:
        _inv, rows = analyse(path, wiki)
        todo = [r for r in rows
                if r["bucket"] in ("A", "B") and not r.get("same") and r.get("proposed")]
        if not todo:
            print("{}: nothing to apply".format(path.name))
            continue

        text = read_exact(path)
        n_items = sum(1 for r in todo if r["kind"] == "item")
        # Mint every id up front, adding each to the taken set so a batch
        # cannot collide with itself.
        taken = used_ids(root)
        ids = []
        for _ in range(n_items):
            fresh = mint(taken)
            taken.add(fresh)
            ids.append(fresh)
        notes, used = [], 0
        # Apply back-to-front: every edit shifts the offsets after it.
        for row in sorted(todo, key=lambda r: r["line"], reverse=True):
            if row["kind"] == "item":
                text, what = apply_item(text, row, ids[used])
                if what == "inserted rules block":
                    used += 1
            else:
                text, what = apply_rule(text, row, None)
            notes.append((row["kind"], row["name"], what))

        bad = [n for n in notes if n[2] in ("id not found", "no insertion point found",
                                            "entry is self-closing, needs manual handling")]
        text, rev = bump_revision(text)
        print("{}: {} edits ({} new rules blocks), revision -> {}{}".format(
            path.name, len(todo), used, rev, "  [{} FAILED]".format(len(bad)) if bad else ""))
        for k, name, what in bad:
            print("   !! {} {}: {}".format(k, name, what))
        if args.write:
            write_exact(path, text)
        else:
            print("   (dry run - pass --write to apply)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
