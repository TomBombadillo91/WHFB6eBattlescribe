"""Shared helpers for the WHFB6e BattleScribe data scripts."""

from __future__ import annotations

import os
import re
import sys
from pathlib import Path

# Data names carry accents and typographic quotes; the Windows console default
# codepage mangles them, so force UTF-8 on the way out.
for _stream in (sys.stdout, sys.stderr):
    try:
        _stream.reconfigure(encoding="utf-8")
    except (AttributeError, ValueError):  # pragma: no cover - non-reconfigurable stream
        pass

ID_RE = re.compile(r"^[0-9a-f]{4}(-[0-9a-f]{4}){3}$")

CAT_NS = "http://www.battlescribe.net/schema/catalogueSchema"
GST_NS = "http://www.battlescribe.net/schema/gameSystemSchema"
IDX_NS = "http://www.battlescribe.net/schema/dataIndexSchema"


def repo_root(override: str | None = None) -> Path:
    """Repo root: <root>/.claude/skills/bsdata-cat/scripts/bsdata.py -> parents[4]."""
    if override:
        return Path(override).resolve()
    env = os.environ.get("BSDATA_ROOT")
    if env:
        return Path(env).resolve()
    here = Path(__file__).resolve()
    for parent in here.parents:
        if (parent / "Deploy").is_dir() and list(parent.glob("*.gst")):
            return parent
    return here.parents[4]


def source_files(root: Path) -> list[Path]:
    """Editable data files in the repo root, game system first."""
    gst = sorted(root.glob("*.gst"))
    cat = sorted(root.glob("*.cat"))
    return gst + cat


def deploy_name(src: Path) -> str:
    return src.stem + (".gstz" if src.suffix == ".gst" else ".catz")


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def root_attr(text: str, name: str) -> str | None:
    """Read an attribute off the root element without parsing the whole file."""
    head = text[:4000]
    m = re.search(r"<(catalogue|gameSystem)\b[^>]*>", head)
    if not m:
        return None
    m2 = re.search(rf'\s{re.escape(name)}="([^"]*)"', m.group(0))
    return m2.group(1) if m2 else None


def strip_ns(tag: str) -> str:
    return tag.split("}")[-1]


def eprint(*args) -> None:
    print(*args, file=sys.stderr)
