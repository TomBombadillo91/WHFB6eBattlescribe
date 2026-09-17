# Checklist: uncategorised entries missing rules text

57 items. Tick as each is done; the box is the source of truth for
what is left if this work is picked up in a later session.

These upgrade entries carry no `categoryLink`, so the magic-item filter in
`wiki_xref.py` never examined them. Each one does have a rules-bearing wiki
page. Same backfill as everywhere else: a `<rules>` block with a fresh id.

## Bretonnians.cat (1)

- [x] `Gromril Great Helm` -> `/magic-item/gromril-great-helm`

## Chaos Dwarves.cat (1)

- [x] `Big'Uns` -> `/special-rules/biguns`

## Daemonic Legions.cat (16)

- [x] `Armour of Khorne` -> `/magic-item/armour-of-khorne`
- [ ] `Axe of Khorne` -> `/magic-item/axe-of-khorne-artifacts-of-the-dark-gods`
- [x] `Chaos Disruption` -> `/magic-item/chaos-disruption`
- [ ] `Collar of Khorne` -> `/magic-item/collar-of-khorne-artifacts-of-the-dark-gods`
- [x] `Gaze of Acquiescence` -> `/magic-item/gaze-of-acquiescence`
- [x] `Master of Sorcery` -> `/magic-item/master-of-sorcery`
- [x] `Might of Khorne` -> `/magic-item/might-of-khorne`
- [x] `Plague Flail` -> `/magic-item/plague-flail`
- [x] `Power Vortex` -> `/magic-item/power-vortex`
- [x] `Radiance of Dark Glory` -> `/magic-item/radiance-of-dark-glory`
- [x] `Soporific Musk` -> `/magic-item/soporific-musk`
- [x] `Soul Hunger` -> `/magic-item/soul-hunger`
- [x] `Spell Breaker` -> `/magic-item/spell-breaker`
- [x] `Spell Destroyer` -> `/magic-item/spell-destroyer`
- [ ] `Stream of Corruption` -> `/magic-item/stream-of-corruption`
- [x] `Tzeentch's Will` -> `/magic-item/tzeentchs-will`

## Dark Elves.cat (1)

- [x] `Chaos Armour` -> `/special-rules/chaos-armour`

## High Elves.cat (1)

- [x] `Power Stone` -> `/magic-item/power-stone`

## Lizardmen.cat (3)

- [x] `Scouts` -> `/special-rules/scouts`
- [x] `Scouts` -> `/special-rules/scouts`
- [x] `Scouts` -> `/special-rules/scouts`

## Tomb Kings.cat (3)

- [x] `Blessing of the Asp` -> `/special-rules/blessing-of-the-asp`
- [x] `Blessing of the Asp` -> `/special-rules/blessing-of-the-asp`
- [x] `Blessing of the Asp` -> `/special-rules/blessing-of-the-asp`

## Vampire Counts.cat (31)

- [x] `Aura of Dark Majesty` -> `/magic-item/aura-of-dark-majesty`
- [x] `Bat Form` -> `/magic-item/bat-form`
- [x] `Beguile` -> `/magic-item/beguile`
- [x] `Blademaster` -> `/magic-item/blademaster`
- [x] `Call Winds` -> `/magic-item/call-winds`
- [x] `Curse of the Revenant` -> `/magic-item/curse-of-the-revenant`
- [x] `Dark Acolyte` -> `/magic-item/dark-acolyte`
- [x] `Domination` -> `/magic-item/domination`
- [x] `Forbidden Lore` -> `/magic-item/forbidden-lore`
- [x] `Heart Piercing` -> `/magic-item/heart-piercing`
- [x] `Honour or Death` -> `/magic-item/honour-or-death`
- [x] `Infinite Hatred` -> `/magic-item/infinite-hatred`
- [x] `Innocence Lost` -> `/magic-item/innocence-lost`
- [x] `Iron Sinews` -> `/magic-item/iron-sinews`
- [x] `Massive Monstrosity` -> `/magic-item/massive-monstrosity`
- [x] `Master Strike` -> `/magic-item/master-strike`
- [x] `Master of the Black Arts` -> `/magic-item/master-of-the-black-arts`
- [x] `Nehekhara's Noble Blood` -> `/magic-item/nehekharas-noble-blood`
- [x] `Quickblood` -> `/magic-item/quickblood`
- [x] `Red Fury` -> `/magic-item/red-fury`
- [x] `Seduction` -> `/magic-item/seduction`
- [x] `Strength of Steel` -> `/magic-item/strength-of-steel`
- [x] `Summon Bats` -> `/magic-item/summon-bats`
- [x] `Summon Ghouls` -> `/magic-item/summon-ghouls`
- [x] `Summon Wolves` -> `/magic-item/summon-wolves`
- [x] `The Awakening` -> `/magic-item/the-awakening`
- [x] `Transfix` -> `/magic-item/transfix`
- [x] `Unholy Cynosure` -> `/magic-item/unholy-cynosure`
- [x] `Wailing Helm` -> `/magic-item/wailing-helm`
- [x] `Walking Death` -> `/magic-item/walking-death`
- [x] `Wolf Form` -> `/magic-item/wolf-form`


## The three left unticked

`Axe of Khorne` and `Collar of Khorne` (x2) each resolve to two wiki pages -
an Artefacts of the Dark Gods version and a Daemonic Gifts version - whose
text differs. The catalogue holds one entry for each. Same modelling question
as Stream of Corruption / Cloud of Flies, so they are carried into
`judgement-calls.xlsx` rather than guessed at here.
