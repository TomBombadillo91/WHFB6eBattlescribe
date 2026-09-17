---
name: bsdata-cat
description: Create and edit BattleScribe catalogue (.cat) and game system (.gst) data files in this WHFB 6th Edition repo — adding or changing units, characters, magic items, special rules, points costs, categories and army-list constraints, and packaging the result into Deploy/. Use whenever the task touches a .cat/.gst file, a .catz/.gstz archive, Deploy/index.xml or index.bsi, or asks about BattleScribe selection entries, entry links, modifiers, conditions, constraints or profiles.
---

# Editing BattleScribe data in this repo

The editable files are the `.cat` and `.gst` in the repo root. `Deploy/` holds the
zipped copies BattleScribe downloads and is **generated** — never hand-edit anything
under it.

## Rules that matter most

1. **Edit the XML as text.** Use targeted `Edit` calls. Do not round-trip a file
   through an XML library to write it back: BattleScribe escapes `'` and `"` as
   `&apos;`/`&quot;`, self-closes empty elements and omits a trailing newline, and
   any serialiser will rewrite thousands of lines you did not touch. Parsing to
   *read* is fine.
2. **Never invent an id.** Every `id`, `targetId`, `childId` and `field` that looks
   like an id must already exist or come from `scripts/new_id.py`. A copied id is
   the single most common way to corrupt one of these files.
3. **Keep child elements in BattleScribe's order** (table in
   [reference/schema.md](reference/schema.md)). Out-of-order children get silently
   rewritten on the next save, turning a one-line change into a huge diff.
4. **Validate before you finish**, and rebuild `Deploy/` as part of the same change.

## Workflow

```bash
# 1. find what you are changing (ids, and who links to them)
python .claude/skills/bsdata-cat/scripts/find_id.py "Great Weapon" --in "Dwarfs.cat"

# 2. mint ids for anything new
python .claude/skills/bsdata-cat/scripts/new_id.py 6

# 3. ... edit the .cat/.gst in the repo root ...

# 4. bump the catalogue revision  (revision="N" on the root element, +1)

# 5. check
python .claude/skills/bsdata-cat/scripts/validate.py "Dwarfs.cat"

# 6. package
python .claude/skills/bsdata-cat/scripts/build_deploy.py
python .claude/skills/bsdata-cat/scripts/validate.py
```

Step 4 is not optional: BattleScribe only offers users an update when the
`revision` in `Deploy/index.xml` goes up, and `build_deploy.py` copies it from the
file header. Bump the `.gst`'s `revision` when you edit the game system; every
catalogue's packaged `gameSystemRevision` is then refreshed automatically.

## Scripts

All under `.claude/skills/bsdata-cat/scripts/`. Python 3, standard library only,
and they locate the repo root themselves.

| Script | What it does |
| --- | --- |
| `find_id.py` | Look up ids by name or names by id, with element kind and location. `--in FILE`, `--tag KIND`. Also `--dump-gst-reference` to regenerate the ID tables. |
| `new_id.py` | Mint ids that collide with nothing in the repo. `new_id.py 6`, or `--check <id>...`. |
| `validate.py` | Dangling `targetId`/`childId`, malformed or duplicated ids, bad `field`/`scope`/`type` values, profile characteristics that disagree with the game system, wrong child order, `Deploy/` drift. Exits non-zero on errors. |
| `build_deploy.py` | Regenerate `Deploy/*.catz`, `*.gstz`, `index.xml`, `index.bsi`. `--check` reports drift without writing. Only rewrites archives whose content actually changed. |
| `wiki_xref.py` | Compare rules text against the scraped 6e wiki and write `reports/`. Never edits. `--only FILE`, `--text <wiki path>` for an XML-ready description, `--numbers` for cost/statline differences, `--stubs` for the undescribed-rule audit. Needs the scrape: `--wiki`, `$WHFB_WIKI_DATA`, or `../6eWikiScraper/data`. |
| `wiki_apply.py` | Apply `wiki_xref.py`'s bucket A/B matches as text surgery. Dry run by default; `--write` to commit the change. Rewrites only the targeted spans, preserving CRLF and BattleScribe escaping. Mints ids for new `<rules>` blocks and bumps the revision. |

A clean checkout is **0 errors, 159 warnings**. Every warning is the known id
collision between `Chaos Dwarves.cat` and `Orcs and Goblins.cat`, which is
deliberately not fixed — see "Accepted validator warnings" in `CLAUDE.md`. Any
error, and any new warning, is yours.

## Reference

* [reference/schema.md](reference/schema.md) — file shape, formatting conventions,
  child element order, and what every element and attribute means.
* [reference/recipes.md](reference/recipes.md) — working XML for the common jobs:
  characters, units, per-model upgrade pricing, mutually exclusive options,
  wizard-only branches, magic item allowances, 0–1 per army, force-org swaps.
* [reference/gamesystem-ids.md](reference/gamesystem-ids.md) — every category,
  characteristic, shared rule and common magic item id from the `.gst`.

## How the pieces fit together

A catalogue's top-level `<selectionEntries>` are the army list: each is a Lord,
Hero, Core, Special or Rare choice, categorised by a `categoryLink` with
`primary="true"`.

* A **unit** is a `type="unit"` entry costing 0 pts, containing a `type="model"`
  child that holds the profile, the per-model cost and the minimum size.
* **Upgrades** are `type="upgrade"` entries, either directly under the unit or
  inside a `selectionEntryGroup` that caps them.
* Anything reused — magic item lists, lores, wizard levels — lives once in
  `<sharedSelectionEntries>` / `<sharedSelectionEntryGroups>` (or in the `.gst`
  when every army has it) and is pulled in with an `entryLink`. Per-army price or
  category overrides go on the **link**, never on the shared target.
* Restrictions are `constraint` (a hard limit) plus `modifier` (change a limit, a
  cost, a stat, a category, or `hidden`) gated by `conditions`. A modifier changes
  a constraint by naming that constraint's `id` in its `field`.

Several catalogues `catalogueLink` to `Dogs of War.cat` with
`importRootEntries="true"`, which merges its entries *and its id namespace* into
theirs — so ids must not collide across a catalogue and anything it links.

## When something does not work in BattleScribe

`validate.py` catches structural faults, not logic ones. If the data loads but
behaves wrongly, check in this order:

* `includeChildSelections="false"` on a condition or constraint that needs to see
  selections nested inside a group — the usual cause of a count that stays at zero.
* `scope="parent"` where the thing being counted is a sibling further up; `ancestor`
  or `roster` may be what you want.
* A `modifier` whose `field` names a constraint id that no longer exists after an
  edit — `validate.py` reports this as an unresolved `field`.
* Hidden entries still counting toward constraints: `hidden` only affects display.
