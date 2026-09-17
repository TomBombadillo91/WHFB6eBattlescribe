#!/usr/bin/env python3
"""Package the editable .cat/.gst files in the repo root into Deploy/.

Reproduces what BattleScribe's own "publish" step produces:

  * every <name>.cat  ->  Deploy/<name>.catz   (zip holding <name>.cat)
  * every <name>.gst  ->  Deploy/<name>.gstz   (zip holding <name>.gst)
  * Deploy/index.xml  regenerated from the file headers
  * Deploy/index.bsi  (zip holding index.xml)

Normalisations applied to the packaged copy only -- the root files are never
rewritten:

  * CRLF -> LF (the repo root is CRLF in the working tree via core.autocrlf)
  * catalogue/@gameSystemRevision refreshed to the .gst's current revision
  * empty <description/> elements dropped, and any element left with no
    children collapsed to a self-closing tag

An archive is only rewritten when its content actually changed, so running the
build twice in a row leaves the working tree clean.

Usage:
    python build_deploy.py            # write Deploy/
    python build_deploy.py --check    # report drift, exit 1 if out of date
    python build_deploy.py --root DIR
"""

from __future__ import annotations

import argparse
import datetime as dt
import re
import sys
import zipfile
from pathlib import Path

from bsdata import IDX_NS, deploy_name, read_text, repo_root, root_attr, source_files

INDEX_HEADER = (
    '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
    '<dataIndex battleScribeVersion="{bsv}" name="{name}" indexUrl="{url}" '
    'xmlns="' + IDX_NS + '">\n'
    "  <dataIndexEntries>\n"
)
INDEX_ENTRY = (
    '    <dataIndexEntry filePath="{path}" dataType="{dtype}" dataId="{did}" '
    'dataName="{dname}" dataBattleScribeVersion="{bsv}" dataRevision="{rev}"/>\n'
)
INDEX_FOOTER = "  </dataIndexEntries>\n</dataIndex>"

EMPTY_DESCRIPTION_RE = re.compile(r"\n[ \t]*<description(?:/>|></description>)")
EMPTY_ELEMENT_RE = re.compile(r"<([A-Za-z]+)([^>]*?)>\s*</\1>")

DEFAULT_INDEX_NAME = "WHFB6eBattlescribe"
DEFAULT_INDEX_URL = (
    "https://raw.githubusercontent.com/TomRome2Rio/WHFB6eBattlescribe/main/Deploy/index.bsi"
)


def normalise(text: str, gs_revision: str | None) -> str:
    text = text.replace("\r\n", "\n")
    text = EMPTY_DESCRIPTION_RE.sub("", text)
    while True:
        collapsed = EMPTY_ELEMENT_RE.sub(r"<\1\2/>", text)
        if collapsed == text:
            break
        text = collapsed
    if gs_revision is not None:
        text = re.sub(
            r'(<catalogue\b[^>]*\sgameSystemRevision=")\d+(")',
            rf"\g<1>{gs_revision}\g<2>",
            text,
            count=1,
        )
    return text


def zip_content(archive: Path, member: str) -> str | None:
    if not archive.exists():
        return None
    try:
        with zipfile.ZipFile(archive) as zf:
            return zf.read(member).decode("utf-8")
    except (KeyError, zipfile.BadZipFile):
        return None


def write_zip(archive: Path, member: str, content: str, mtime: float) -> None:
    info = zipfile.ZipInfo(member, dt.datetime.fromtimestamp(mtime).timetuple()[:6])
    info.compress_type = zipfile.ZIP_DEFLATED
    info.external_attr = 0o600 << 16
    archive.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(archive, "w") as zf:
        zf.writestr(info, content.encode("utf-8"))


def index_preamble(deploy: Path) -> tuple[str, str, list[str]]:
    """Reuse the existing index's name/url and entry order so diffs stay small."""
    existing = deploy / "index.xml"
    if not existing.exists():
        return DEFAULT_INDEX_NAME, DEFAULT_INDEX_URL, []
    text = read_text(existing)
    name = re.search(r'<dataIndex\b[^>]*\sname="([^"]*)"', text)
    url = re.search(r'<dataIndex\b[^>]*\sindexUrl="([^"]*)"', text)
    order = re.findall(r'<dataIndexEntry\s+filePath="([^"]+)"', text)
    return (
        name.group(1) if name else DEFAULT_INDEX_NAME,
        url.group(1) if url else DEFAULT_INDEX_URL,
        order,
    )


def build_index(deploy: Path, sources: list[Path]) -> str:
    name, url, order = index_preamble(deploy)
    entries: dict[str, str] = {}
    for src in sources:
        text = read_text(src)
        path = deploy_name(src)
        entries[path] = INDEX_ENTRY.format(
            path=path,
            dtype="gamesystem" if src.suffix == ".gst" else "catalogue",
            did=root_attr(text, "id"),
            dname=root_attr(text, "name"),
            bsv=root_attr(text, "battleScribeVersion"),
            rev=root_attr(text, "revision"),
        )
    ordered = [p for p in order if p in entries]
    ordered += [p for p in entries if p not in ordered]
    body = "".join(entries[p] for p in ordered)
    return INDEX_HEADER.format(bsv="2.03", name=name, url=url) + body + INDEX_FOOTER


def put(path: Path, text: str, crlf: bool, check: bool, changed: list[str]) -> None:
    data = (text.replace("\n", "\r\n") if crlf else text).encode("utf-8")
    if path.exists() and path.read_bytes() == data:
        return
    changed.append(path.name)
    if not check:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)


def main() -> int:
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    ap.add_argument("--root", help="repo root (default: auto-detected)")
    ap.add_argument("--check", action="store_true", help="report drift without writing")
    args = ap.parse_args()

    root = repo_root(args.root)
    deploy = root / "Deploy"
    sources = source_files(root)
    if not sources:
        print(f"no .cat/.gst files found under {root}", file=sys.stderr)
        return 2

    gst = next((s for s in sources if s.suffix == ".gst"), None)
    gs_revision = root_attr(read_text(gst), "revision") if gst else None

    changed: list[str] = []
    for src in sources:
        content = normalise(read_text(src), gs_revision if src.suffix == ".cat" else None)
        archive = deploy / deploy_name(src)
        if zip_content(archive, src.name) == content:
            continue
        changed.append(archive.name)
        if not args.check:
            write_zip(archive, src.name, content, src.stat().st_mtime)

    index_xml = build_index(deploy, sources)
    existing = deploy / "index.xml"
    crlf = b"\r\n" in existing.read_bytes() if existing.exists() else False
    put(existing, index_xml, crlf, args.check, changed)

    bsi = deploy / "index.bsi"
    if zip_content(bsi, "index.xml") != index_xml:
        changed.append(bsi.name)
        if not args.check:
            write_zip(bsi, "index.xml", index_xml, existing.stat().st_mtime)

    if not changed:
        print(f"Deploy/ up to date ({len(sources)} data files)")
        return 0
    verb = "out of date" if args.check else "wrote"
    print(f"{verb}: {', '.join(sorted(set(changed)))}")
    return 1 if args.check else 0


if __name__ == "__main__":
    raise SystemExit(main())
