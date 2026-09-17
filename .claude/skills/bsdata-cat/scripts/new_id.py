#!/usr/bin/env python3
"""Mint BattleScribe IDs that collide with nothing in the repo.

Every id, targetId, childId and constraint id in a BattleScribe file is four
lowercase hex quads (`1a2b-3c4d-5e6f-7a8b`). Ids have to be unique across every
file that can be loaded into the same roster, so these are drawn at random and
checked against every .cat and .gst in the repo root.

Usage:
    python new_id.py            # one id
    python new_id.py 12         # twelve ids, one per line
    python new_id.py --check 1a2b-3c4d-5e6f-7a8b [...]
    python new_id.py --root DIR
"""

from __future__ import annotations

import argparse
import re
import secrets
import sys

from bsdata import ID_RE, read_text, repo_root, source_files


def used_ids(root) -> set[str]:
    seen: set[str] = set()
    for path in source_files(root):
        seen.update(re.findall(r'\sid="([^"]+)"', read_text(path)))
    return seen


def mint(taken: set[str]) -> str:
    while True:
        candidate = "-".join(secrets.token_hex(2) for _ in range(4))
        if candidate not in taken:
            return candidate


def main() -> int:
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    ap.add_argument("count", nargs="?", type=int, default=1, help="how many ids (default 1)")
    ap.add_argument("--check", nargs="+", metavar="ID", help="report whether these ids are free")
    ap.add_argument("--root", help="repo root (default: auto-detected)")
    args = ap.parse_args()

    root = repo_root(args.root)
    taken = used_ids(root)

    if args.check:
        bad = False
        for candidate in args.check:
            if not ID_RE.match(candidate):
                print(f"{candidate}: malformed (want four lowercase hex quads)")
                bad = True
            elif candidate in taken:
                print(f"{candidate}: ALREADY USED")
                bad = True
            else:
                print(f"{candidate}: free")
        return 1 if bad else 0

    if args.count < 1:
        print("count must be at least 1", file=sys.stderr)
        return 2

    minted: set[str] = set()
    for _ in range(args.count):
        new = mint(taken | minted)
        minted.add(new)
        print(new)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
