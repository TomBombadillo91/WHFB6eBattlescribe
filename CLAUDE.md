# WHFB6eBattlescribe

BattleScribe 2.03 data files for Warhammer Fantasy Battle 6th edition, published
as a BSData-style repository that BattleScribe fetches over HTTP.

## Layout

| Path | What it is |
| --- | --- |
| `*.cat` (repo root) | The editable army catalogues — one per army book. **Edit these.** |
| `Warhammer Fantasy 6th Edition.gst` | The game system: force organisation, categories, profile types, common magic items, shared special rules. **Edit this.** |
| `Deploy/` | Generated. Zipped `.catz`/`.gstz` copies plus `index.xml` and `index.bsi`, served from `main` via raw.githubusercontent.com. **Never hand-edit.** |
| `Battlescribe/` | The BattleScribe 2.03.21 installer, kept for convenience. |
| `.claude/skills/bsdata-cat/` | Skill and scripts for working on the data files. |

The data files are large XML documents (100k–700k, up to 10k lines). Search them
with Grep or `find_id.py` rather than reading them whole.

## Working on the data

Use the **`bsdata-cat` skill** — it holds the schema reference, editing recipes,
the game system's ID tables, and the scripts below. In short:

```bash
python .claude/skills/bsdata-cat/scripts/find_id.py "Great Weapon" --in "Dwarfs.cat"
python .claude/skills/bsdata-cat/scripts/new_id.py 6      # ids for new elements
# ... edit the .cat, bump its revision ...
python .claude/skills/bsdata-cat/scripts/validate.py
python .claude/skills/bsdata-cat/scripts/build_deploy.py
```

Non-negotiables:

* Edit the XML as **text**, with targeted edits. Do not reserialise a file through
  an XML library — BattleScribe's escaping and formatting conventions will not
  survive, and the diff becomes unreviewable.
* Every new `id` comes from `new_id.py`. Never reuse or hand-type one.
* Bump the root element's `revision` on any file you change; that is what tells
  BattleScribe an update is available.
* Keep root `.cat`/`.gst` and `Deploy/` in the same commit.

## Line endings

`core.autocrlf=true`: the root data files are CRLF in the working tree and LF in
git. The copies inside `Deploy/*.catz` are always LF. `build_deploy.py` handles
this; do not "fix" line endings by hand.

## Commits

Short lowercase imperative subjects, matching the existing history
(`fixup wood elf amber pendant points cost`, `Add Ogre Kingdoms`,
`Chorf Bugfixes + Powerstone fixup`). One army or one theme per commit. Mention
the army by name so the log stays greppable.

A data change is one commit containing the edited root file **and** the regenerated
`Deploy/` artefacts. Run `validate.py` and `build_deploy.py --check` before
committing; `--check` exiting non-zero means `Deploy/` is stale.

## Accepted validator warnings

A clean checkout validates with **0 errors** and 159 warnings. The warnings are all
the same known condition, deliberately left alone:

* 159 ids are shared between `Chaos Dwarves.cat` and `Orcs and Goblins.cat`.
  Chaos Dwarves was added first (2023-05-22) and Orcs and Goblins was built the
  next day by copying its structure without re-minting ids, so the same id is
  `Chaos Dwarf Lord` in one file and `Black Orc Warboss` in the other.

  This is inert: neither catalogue `catalogueLink`s the other and 6th edition has
  no allies, so the two are never loaded into one roster. Re-minting either side
  would invalidate ~44 entries in every saved `.rosz` for that army, which costs
  more than it buys. **Leave it.** The warning is the guard — if a future change
  ever links these two catalogues, `validate.py` escalates it to an error.

Do not add new warnings to either file, and treat any *error* as yours.
