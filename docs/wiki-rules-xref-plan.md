# Cross-reference and backfill WHFB 6e rules text from the wiki scrape

## Context

`C:\src\WHFB6eBattlescribe` publishes BattleScribe data for WHFB 6th edition. Its rules
text was transcribed by hand from the printed army books over several years, by different
people, to no consistent standard. The result is uneven:

* Some descriptions are accurate but heavily abbreviated. `Dwarfs.cat` renders Ancestral
  Grudge as *"All Dwarfs Hate all types of Greenskins (Orcs, Goblins, Snotlings, Night
  Goblins, Black Orcs, Hobgoblins, etc.)"* where the source rule is a full paragraph.
* Some contain transcription errors. `Dwarfs.cat` has a rule named
  **`Master Rune of Switftness`** — a typo for *Swiftness*, found in the first five minutes
  of investigating this.
* Whole armies have no item text at all. In `Vampire Counts.cat`, `Cursed Book` is a bare
  `selectionEntry` with a 50pt cost, a category and two constraints — a player who selects
  it sees a name and a price and nothing else. Bretonnians, Tomb Kings and Daemonic Legions
  are the same.
* `Lizardmen.cat:3` admits it: `<readme>WIP Lizardmen. TODO: Add unit profiles & item
  descriptions</readme>`.

`C:\src\6eWikiScraper` now mirrors <https://6th.whfb.app> as 3,437 Markdown pages plus a
name-keyed cross-reference index built for exactly this job. We treat the wiki as the source
of truth.

**Intended outcome:** every army-book rule, magic item and spell in the catalogues carries
the wiki's rules text, verbatim and complete; and every place the catalogues disagree with
the wiki on a number is written up for the maintainer to adjudicate.

**Non-goals.** Core rulebook mechanics (movement, shooting, close combat, the turn
sequence, the appendices, the glossary) stay out of the catalogues, with one exception: see
Phase E. Army composition constraints, points values and list structure are **not** touched
— this is a rules-text project.

---

## Decisions already taken

These were settled with the maintainer. Do not revisit them.

| Question | Decision |
| --- | --- |
| Terse-but-correct descriptions | **Normalise all of them to the wiki's text.** Consistency across catalogues is the goal, not a minimal diff. |
| Flavour / background prose | **Exclude.** Descriptions carry mechanical text only. See Phase C for the split rule. |
| Points costs and statlines | **Report only, do not change.** Produce a discrepancy list for the maintainer to check by hand. |
| Core rules named as unit special rules (Fear, Hatred, Frenzy, Stupidity, Immune to Psychology…) | **Add once to the `.gst` as shared rules and `infoLink` them**, never duplicate per catalogue. |

---

## Baseline measurements

Confirmed by parsing both repos; re-derive rather than trusting these if they look stale.

**BattleScribe side** — 16 `.cat` + 1 `.gst`, 1,227 `<rule>` elements:

* 1,120 have a non-empty `<description>`; 106 have no `<description>` child; 1 is empty
  (`Daemonic Legions.cat:2692`).
* All 644 `<profile>`s are `typeName="Model"` — every one is an M/WS/BS/S/T/W/I/A/Ld
  statline. There is no weapon or magic-item profile type. **Prose lives only in
  `rule/description`.** Nothing else in these files is text worth diffing.
* Of 2,317 `type="upgrade"` selection entries, 1,454 have no `<rules>`, `<profiles>` or
  `<infoLinks>` at all. Narrowing to entries in a magic-item-ish category: **236 of 658
  carry no text whatsoever.**

| Catalogue | Magic-item entries with no text |
| --- | ---: |
| `Bretonnians.cat` | 89 |
| `Forces of Chaos.cat` | 59 |
| `Tomb Kings.cat` | 34 |
| `Vampire Counts.cat` | 32 |
| `Dark Elves.cat` | 11 |
| `Daemonic Legions.cat` | 7 |
| `Skaven.cat` | 4 |
| *(the other nine)* | 0 |

Rule-stub counts concentrate the same way: `Daemonic Legions.cat` 21 undescribed rules,
`Forces of Chaos.cat` 22, `Tomb Kings.cat` 15, `Vampire Counts.cat` 13, `Lizardmen.cat` 10.

**Wiki side** — `C:\src\6eWikiScraper\data`, 3,437 pages: 1,444 `rule`, 923 `magic-item`,
789 `unit`, 162 `spell`, 20 `army`. `manifest.json` reports `failures: {}`.

**Match rate** — normalising catalogue rule names through the scraper's own `normalise()`
and testing them against `index.json`'s `lookup` table hits an exact key for **~90%** of
names (e.g. Dark Elves 109/126, Wood Elves 80/95, Dogs of War 29/39).

---

## Deliverables

1. `.claude/skills/bsdata-cat/scripts/wiki_xref.py` — the reconciliation tool (Phase A).
2. A triage report per army under `reports/` (Phase B) — reviewed, then consumed by Phase D.
3. Edited `.cat`/`.gst` files plus regenerated `Deploy/`, one commit per army (Phases D–E).
4. `reports/numeric-discrepancies.md` — the statline and points-cost differences, for the
   maintainer. **Not applied.** (Phase F.)
5. `reports/left-undescribed.md` — every rule deliberately left without text, and why.
   **Not applied.** (Phase G.)

---

## Phase A — build the reconciliation tool

Add `wiki_xref.py` to `.claude/skills/bsdata-cat/scripts/`, alongside the existing
`find_id.py` / `new_id.py` / `validate.py` / `build_deploy.py`. Reuse `bsdata.py`'s
`repo_root()`, `source_files()`, `read_text()` and its UTF-8 stdout forcing — the Windows
console will mangle accented data names otherwise.

```bash
python .claude/skills/bsdata-cat/scripts/wiki_xref.py \
    --wiki C:/src/6eWikiScraper/data --out reports/
```

**Do not re-implement name normalisation.** The `lookup` keys in `index.json` were built by
`whfb6e.indexer.normalise()`; any other folding silently misses matches. Either
`sys.path.insert` the scraper repo and import it, or vendor the function verbatim with a
comment naming its origin. Take `--wiki` as a parameter with a sensible default; do not
hard-code an absolute path.

### Extract from the catalogues

Parse with `ElementTree` for *analysis only* (see the editing constraint in Phase D). For
each of the 16 catalogues plus the `.gst`, collect:

* every `<rule>`: `name`, `id`, source file, line number, description text, and its owner
  (unit `selectionEntry` / `sharedRules` / `infoGroup` / catalogue root);
* every `type="upgrade"` `selectionEntry` in a magic-item category that has no `<rules>`,
  `<profiles>` or `<infoLinks>` — these are the Phase D additions;
* every `Model` profile's name and nine characteristics — for Phase F;
* every `<cost name="pts">` on a magic-item entry — for Phase F.

### Match against the wiki

Match **globally against the whole `lookup` table**, not within the army's association.
An association-scoped match was tried and is wrong: it scores `Dogs of War.cat` at 1/39
because Dogs of War content is tagged `Regiments of Renown` on the wiki. Use `association`
as a *confirmation* signal instead (below).

Classify every catalogue rule name into exactly one bucket:

| Bucket | Test | Handling |
| --- | --- | --- |
| **A — exact** | `normalise(name)` is a key in `lookup`, single hit, or multiple hits where one has `match: "page"` | Auto-apply in Phase D |
| **B — variant** | No exact key, but a *deterministic* rewrite hits one: drop a leading `The `, singular↔plural, strip a trailing `(…)` parenthetical | Auto-apply, but list the rewrite in the report |
| **C — ambiguous** | Several `match: "page"` hits, or the best hit's `association` does not include this army | Human decision, listed with all candidates |
| **D — mechanical tag** | Matches `Unit Strength N`, `Armour Save (N+)`, `Ward Save (N+)`, `Scaly Skin (N+)`, `Impact Hits (…)`, `Flying Unit (…)`, `Level N Wizard` | **Skip.** BattleScribe display labels, not rules. Leave undescribed, and record in Phase G. |
| **E — no coverage** | No hit at any confidence | Report as "wiki does not cover this"; leave the existing text alone, and record in Phase G |

**The tool must never auto-apply a fuzzy match.** `RulesIndex.find()`'s `difflib` fallback
is actively dangerous here — it maps `Doomwheel` → `/movement/wheel`, `Ironfist` →
`Garagrim Ironfist` (a Dwarf character), and `Hate High Elves` → `/army/high-elves`. Run
fuzzy matching only to *populate the candidate list* for buckets C and E, always with the
score printed, and never as the basis for a write.

Bucket B is worth getting right: `Grail Vow` → *The Grail Vow*, `Questing Vow` → *The
Questing Vow*, `Undead Constructs` → *Undead Construct* are all real matches that exact
keying alone misses.

### Report format

One Markdown file per army under `reports/`, plus `reports/summary.md`. Each row needs:
catalogue name and line, bucket, wiki path, whether the existing text already equals the
proposed text, and a unified diff when it does not. Record `index.json`'s `build_id` and
`generated_at` in every report header — the scraper repo has no commits yet, so the report
itself is the only provenance for which wiki revision a change came from.

---

## Phase B — triage

Run the tool, read `reports/summary.md`, and hand buckets C and E to the maintainer before
editing anything. Expect roughly 100–150 rows across all armies. Resolve C by picking a wiki
path per row; resolve E by confirming the existing text stands.

Catalogues divide into three shapes, and the work differs by shape:

* **Complete** — Dwarfs, High Elves, Lizardmen, Ogre Kingdoms, Orcs & Goblins, The Empire,
  Wood Elves, Chaos Dwarves, Dogs of War. Every magic item already has text. Work here is
  normalisation and error-fixing only.
* **Empty** — Bretonnians, Tomb Kings, Vampire Counts, Daemonic Legions. No magic item has
  text. Work here is bulk addition.
* **Partial** — Forces of Chaos, Dark Elves, Skaven. Both.

---

## Phase C — converting a wiki page into a `<description>`

This is the conversion contract. Apply it identically everywhere.

**1. Take the body, drop the scaffolding.** Use `RulesIndex.text(path)` to get the Markdown
with front matter stripped, then discard the `# Title` heading and the `## Related`,
`## Referenced by`, `## Special Rules` and `## Profile` sections. What remains is the rule.

**2. Drop flavour paragraphs.** Wiki pages open with a background paragraph before the
mechanical text. Ancestral Grudge:

> ~~Dwarfs hold grudges for a long time, possibly forever. They have never forgiven the fall
> of their strongholds at the hands of the Orcish enemy.~~
>
> Dwarfs hate all types of Orcs, Goblins and Snotlings, including Night Goblins, Black Orcs,
> Hobgoblins... In fact all greenskins of any description!

Keep only the second. The signal for a *rules* paragraph is the presence of dice notation
(`D6`, `2D6`), a measurement (`6"`), a characteristic abbreviation, a points value, or a
game keyword (`save`, `ward`, `wound`, `attack`, `casting`, `charge`, `panic`, `hate`,
`fear`, `terror`, `bound spell`, `one use only`, `may`, `must`, `re-roll`, `+1`, `-1`).
Treat this as a **heuristic the tool flags and the agent confirms**, not as a rule the tool
applies unsupervised — the classifier will be wrong often enough to matter over ~1,100
descriptions. Where the whole page is mechanical, keep all of it.

**3. Flatten links to their text.** `[hate](../psychology/hatred.md)` → `hate`. BattleScribe
descriptions are plain text; a stray Markdown link is a visible artefact in a roster.

**4. Flatten tables to tab-separated lines.** This convention already exists — compare
`data/pages/special-rules/organ-gun-misfire-chart.md` with the `Organ Gun Misfire` rule in
`Dwarfs.cat`, which stores the same chart as `D6\t\tResult` and one tab-separated line per
row. Drop the GFM `| --- |` separator row.

**5. Separate paragraphs with a blank line**, matching existing descriptions.

**6. Escape for XML as BattleScribe does**: `"` → `&quot;`, `'` → `&apos;`, `&` → `&amp;`,
`<` → `&lt;`. Check the result round-trips — `Flakkson's Rune of Seeking` is stored as
`Flakkson&apos;s Rune of Seeking`, and any matching code that forgets to unescape will
report a false miss.

**Preserve the wiki's own typos.** The scrape carries OCR artefacts from the printed books
("The gun explode", "Perhap", "mishanthed"). The wiki is the source of truth; copying it
faithfully keeps the two sources diffable in future. Do not silently correct it. If a typo
is egregious, note it in the report rather than fixing it inline.

---

## Phase D — apply, one army per commit

Follow `CLAUDE.md` and the `bsdata-cat` skill. The binding constraints:

* **Edit the XML as text**, with targeted `Edit` calls. Never write a file back through
  `ElementTree` — BattleScribe's escaping and formatting will not survive and the diff
  becomes unreviewable. `ElementTree` is for reading and reporting only.
* **Every new `id` comes from `new_id.py`.** Adding text to a bare magic-item entry means
  adding a `<rules><rule id="…">` block, and that rule needs a freshly minted id. Never
  hand-type or reuse one.
* **Bump the root element's `revision`** on every file touched.
* Root file and `Deploy/` go in the **same commit**.

### Per army

1. Rewrite bucket A/B descriptions to the Phase C text.
2. Apply the maintainer's bucket C resolutions.
3. For each of the 236 magic-item entries with no text, insert a `<rules>` block holding a
   single `<rule>` named exactly as the `selectionEntry`. Mirror the existing pattern — see
   `Dispel Scroll` at `Warhammer Fantasy 6th Edition.gst:297-302`, which is a
   `selectionEntry` wrapping a same-named `rule`. Respect the schema's child ordering;
   `validate.py` checks it.
4. Fill rule stubs that are genuine gaps. **Leave deliberate stubs alone** — a self-closing
   `<rule … />` whose name also exists as a described rule in the `.gst`'s `<sharedRules>`,
   or which matches the bucket-D tag patterns, is intentional. The `.gst`'s bare `Skirmishers`
   (`:627`) sits between two fully-described rules; that is a decision, not an oversight.
   **Every rule you leave undescribed goes on the Phase G list**, with the reason.
5. `python .claude/skills/bsdata-cat/scripts/validate.py` → 0 errors, 159 warnings.
6. `python .claude/skills/bsdata-cat/scripts/build_deploy.py`
7. Commit: short lowercase imperative, army named, e.g.
   `backfill vampire counts magic item rules text from wiki`.

### Two traps

* **50 rule names carry more than one distinct description** across the repo — `Mark of
  Khorne` has 8 variants inside `Forces of Chaos.cat` alone, `Mark of Slaanesh` 7 across two
  files. A name-keyed join is not 1:1. Key edits on rule **`id`**, never on name.
* **Five `<modifier field="description">` elements override the stored text at runtime** —
  `Lizardmen.cat:2031` and `Forces of Chaos.cat:7336,7341,7346,7351`. Rewriting the
  `<description>` under one of these changes only the fallback. Check each by hand and
  update the modifier `value` to match.

Suggested order: start with **Vampire Counts** (22 rules, 32 items — small, and the worst
gap, so it validates the whole pipeline on a real case), then the other three empty
catalogues, then the three partial ones, then the nine complete ones for normalisation.

---

## Phase E — core rules into the game system

The catalogues name core psychology rules as unit special rules. Add these **once** to
`<sharedRules>` in `Warhammer Fantasy 6th Edition.gst`, then `infoLink` them by `targetId`
from the catalogues that reference them.

Scope it to names the catalogues already use — do not import the rulebook wholesale. Get
the list from the tool: any catalogue rule name whose wiki hit sits under the `psychology`,
`special-rules` or `close-combat` sections with `association: Main Rulebook`. Several are
already there (`Fear` at `:673`, `Immune to Psychology` at `:512a-…`); those need their text
normalised, not re-adding. Note the `.gst`'s existing text is OCR-damaged — `Terror` reads
"d1at causes terror", `Fly` reads "me ground" — so these are corrections, not just additions.

The chain to follow is `Scouts`: defined at `Warhammer Fantasy 6th Edition.gst:620` with
`id="ec06-621f-83ae-fd4c"`, referenced from `Dwarfs.cat:1110` by an `<infoLink>` carrying
its own fresh id and that `targetId`. Eight catalogues link the same id. Use
`find_id.py <id>` for the reverse lookup.

Commit separately: `normalise core special rules text in game system`.

---

## Phase F — numeric discrepancy report

Report only. **Change nothing.** Write `reports/numeric-discrepancies.md`.

**Magic item points costs.** The wiki carries `points_cost` on all 923 magic-item pages.
Diff against `<cost name="pts">` on the matched `selectionEntry`. Git history shows this
class of bug is real (`fixup wood elf amber pendant points cost`).

**Unit statlines.** The wiki carries a `statistics` block for all 789 unit pages. Diff
against the nine `<characteristic>` values of the matched `Model` profile.

**A hard limit to state in the report:** the wiki has **no points costs for units,
equipment or upgrades** — only for magic items. Unit costs cannot be validated against this
source. Do not imply otherwise.

Two further caveats to carry into the report: 84 of 88 weapon pages lost their profile
table (the wiki embedded it as a chart entry with no page, which is most of
`manifest.json`'s `unresolved_link_count: 506`); and army-list pages are structural only —
no points, no min/max, no equipment options.

Group by army, sort by size of difference, and state for each row which side says what.
Do not editorialise about which is correct.

---

## Phase G — audit list of rules left undescribed

Report only. **Change nothing.** Write `reports/left-undescribed.md`.

Every decision to leave a rule without text must be recorded, so the maintainer can confirm
after the fact that each one was appropriate. A rule silently skipped is indistinguishable
from a rule missed; this list is what makes the difference auditable.

Cover **every** `<rule>` that still has no `<description>` once Phases D and E are complete
— both the ones that were already bare and any the agent chose not to fill. One row each:

| Column | Contents |
| --- | --- |
| Rule | Name, `id`, catalogue and line |
| Reason | One of the five below |
| Wiki coverage | The wiki path if one exists at any confidence, else `none` — **with the match score** |
| Resolves to | For `shared-rule` rows, the `targetId` and the file:line of the described rule it links to |

The five reasons, which the tool should assign mechanically:

1. **`mechanical-tag`** — bucket D. A BattleScribe display label (`Unit Strength 5`,
   `Ward Save (5+)`, `Scaly Skin (4+)`, `Impact Hits (D6+2)`, `Level 3 Wizard`). No rules
   text exists to add.
2. **`shared-rule`** — the name resolves to a described rule elsewhere, so text here would be
   duplication. The `.gst`'s bare `Skirmishers` (`:627`) is the canonical case.
3. **`core-rule`** — core rulebook content held out of the catalogues by the Phase E scope
   decision.
4. **`no-coverage`** — bucket E. The wiki has nothing at any confidence.
5. **`deferred`** — the agent judged the wiki text a poor fit, or the maintainer's bucket C
   resolution said to leave it. Give the reason in prose; this column should be short.

**Sort the file with `no-coverage` and `deferred` first, then any row whose Wiki coverage
column is not `none`.** Those are the rows worth a human's time. A `mechanical-tag` row with
no wiki coverage is self-evidently fine and should not crowd out the interesting ones.

Two checks to flag inline, because they are where a wrong call hides:

* **A `shared-rule` row whose `targetId` is absent or points at a rule that is itself
  undescribed** is a broken assumption, not a deliberate omission. Mark it.
* **A `mechanical-tag` or `core-rule` row that *does* have wiki coverage** means text was
  available and deliberately not used. That may well be right, but it is the category most
  likely to contain a mistake, so call it out rather than burying it.

Expect on the order of 110–130 rows: 106 rules currently have no `<description>`, plus
whatever Phases D and E decline to fill, minus those they do.

---

## Verification

After each army's commit:

```bash
python .claude/skills/bsdata-cat/scripts/validate.py
```

0 errors and exactly 159 warnings — those 159 are the known shared ids between
`Chaos Dwarves.cat` and `Orcs and Goblins.cat`, documented in `CLAUDE.md`. **A new warning
means you introduced one.** Any error is yours.

```bash
python .claude/skills/bsdata-cat/scripts/build_deploy.py --check
```

Must exit zero, proving `Deploy/` is not stale.

Re-run `wiki_xref.py` and confirm the army's bucket A/B rows now report the existing text as
equal to the proposed text — that is the end-to-end check that the edit landed as intended.

Then load the army in BattleScribe (`Battlescribe/` holds the 2.03.21 installer), build a
roster containing at least one edited magic item and one edited special rule, and confirm
the text displays correctly and with no Markdown or escaping artefacts. Do this at least
once on the first army before committing to the pattern across all sixteen.

Once every army is done, regenerate `reports/left-undescribed.md` (Phase G) against the
final state of the repo and read it. It is the last chance to catch a rule that was skipped
rather than judged.

Finally, the whole-repo check before the last commit: `validate.py` clean, `build_deploy.py
--check` clean, and `git diff --stat` showing root file and `Deploy/` moving together.

## Risks

* **Volume.** ~1,100 descriptions normalised plus 236 items added is large. Per-army commits
  keep each reviewable; do not batch armies together.
* **The wiki scrape is not version-pinned** — `C:\src\6eWikiScraper` has no commits. Record
  `build_id` in every report so a future re-run can tell whether a difference is a wiki
  change or a regression.
* **Flavour/rules splitting is a judgment call** at scale. Budget a review pass; spot-check
  a sample per army rather than trusting the classifier.
* **Bucket E may hide real errors.** A name with no wiki coverage at any confidence might be
  a misspelling like `Master Rune of Switftness` rather than genuinely uncovered content.
  Read that list; do not just archive it.
