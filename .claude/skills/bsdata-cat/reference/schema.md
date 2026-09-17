# BattleScribe 2.03 `.cat` / `.gst` schema, as this repo uses it

Everything below was derived from the files in this repo, so it reflects what
BattleScribe 2.03.21 actually writes rather than what the published XSD permits.

## File shape

```xml
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<catalogue id="c189-c206-4913-5be6" name="Dwarfs" revision="2" battleScribeVersion="2.03"
           library="false" gameSystemId="4ca8-2035-2f87-1bd7" gameSystemRevision="25"
           xmlns="http://www.battlescribe.net/schema/catalogueSchema">
  ...
</catalogue>
```

* UTF-8, two-space indent, **no trailing newline**, CRLF in the working tree.
* `<` `>` `&` `"` `'` in text and attributes are all escaped — BattleScribe writes
  `&quot;` and `&apos;` even where XML does not require them. Match that when you
  hand-write descriptions, or the next BattleScribe save will rewrite your lines.
* Empty elements are self-closing: `<rule id="..." name="Skirmishers" hidden="false"/>`,
  never `<rule ...></rule>`.
* The `.gst` root is `<gameSystem>` with the `gameSystemSchema` namespace; it has no
  `gameSystemId`/`library` and adds `authorName`/`authorContact`/`authorUrl`.

## Child element order

BattleScribe writes children in a fixed order and rewrites the file if you get it
wrong. `validate.py` checks this.

| Parent | Order |
| --- | --- |
| `gameSystem` | `readme`, `publications`, `costTypes`, `profileTypes`, `categoryEntries`, `forceEntries`, `selectionEntries`, `entryLinks`, `rules`, `sharedSelectionEntries`, `sharedSelectionEntryGroups`, `sharedRules`, `sharedProfiles`, `sharedInfoGroups` |
| `catalogue` | `readme`, `publications`, `costTypes`, `categoryEntries`, `selectionEntries`, `entryLinks`, `rules`, `infoLinks`, `sharedSelectionEntries`, `sharedSelectionEntryGroups`, `sharedRules`, `sharedProfiles`, `sharedInfoGroups`, `catalogueLinks` |
| `selectionEntry` | `modifiers`, `modifierGroups`, `constraints`, `profiles`, `rules`, `infoGroups`, `infoLinks`, `categoryLinks`, `selectionEntries`, `selectionEntryGroups`, `entryLinks`, `costs` |
| `selectionEntryGroup` | same as `selectionEntry`, minus `costs` |
| `entryLink` | `modifiers`, `modifierGroups`, `constraints`, `profiles`, `rules`, `infoGroups`, `infoLinks`, `categoryLinks`, `costs` |
| `categoryEntry` | `modifiers`, `modifierGroups`, `constraints`, `profiles`, `rules`, `infoGroups`, `infoLinks` |
| `categoryLink` | `modifiers`, `modifierGroups`, `constraints` |
| `profile` | `modifiers`, `modifierGroups`, `characteristics` |
| `rule` | `modifiers`, `modifierGroups`, `description` |
| `infoGroup` | `modifiers`, `modifierGroups`, `profiles`, `rules`, `infoLinks` |
| `modifier` | `repeats`, `conditions`, `conditionGroups` |
| `modifierGroup` | `comment`, `repeats`, `conditions`, `conditionGroups`, `modifiers`, `modifierGroups` |
| `conditionGroup` | `conditions`, `conditionGroups` |

## IDs

Four lowercase hex quads: `1a2b-3c4d-5e6f-7a8b`. Every `id` must be unique across
all files loaded into one roster — that is the catalogue, the `.gst`, and every
catalogue reached through `catalogueLinks`. Mint them with `scripts/new_id.py`;
never hand-type or copy one.

Note `constraint/@id` is a real id: `modifier/@field` points at it to change a
limit, so the two have to agree.

## The building blocks

### `selectionEntry`

```xml
<selectionEntry id="..." name="Hammerers" hidden="false" collective="false"
                import="true" type="unit" page="27" publicationId="d9e7-...">
```

* `type` — `model` (a single figure with a profile), `unit` (a container whose
  children are the models), `upgrade` (equipment, command, magic item, level).
* `hidden` — hides it from the UI; usually flipped by a `modifier`, not set here.
* `collective` — `true` collapses identical child selections into one line. This
  repo leaves it `false` everywhere.
* `import` — `true` lets other catalogues link to it; leave it `true`.
* `page` / `publicationId` — optional source citation; publication ids live in
  the `.gst`.

Top-level army list entries live in `<selectionEntries>` directly under
`<catalogue>`. Things reused across entries live in `<sharedSelectionEntries>` /
`<sharedSelectionEntryGroups>` and are pulled in by `entryLink`.

### `selectionEntryGroup`

A chooser — "Weapon", "Command", "Magic Items". `defaultSelectionEntryId` preselects
one of its own options. Constraints on the group limit the whole chooser
(`max 1` makes the options mutually exclusive).

### `entryLink` and `infoLink`

`entryLink` reuses a selection entry or group; `infoLink` reuses a rule, profile or
info group.

```xml
<entryLink id="..." name="General" hidden="false" collective="false" import="true"
           targetId="cf7b-798c-9b94-df74" type="selectionEntry"/>
<infoLink id="..." name="Fly" hidden="false" targetId="87db-2d4c-3fa6-6a26" type="rule"/>
```

`type` is `selectionEntry` / `selectionEntryGroup` for `entryLink`, and
`rule` / `profile` / `infoGroup` for `infoLink`. A link can carry its own
`constraints`, `modifiers`, `categoryLinks` and `costs`, which layer on top of the
target — that is how a shared magic item gets a per-army price or category.

The `name` on a link is cosmetic; keep it equal to the target's name so searches work.

### `categoryLink`

Puts the entry in a force-organisation or item category. Exactly one should be
`primary="true"` — that is the slot it consumes (Core/Special/Rare/Lords/Heroes).
Category ids are in [gamesystem-ids.md](gamesystem-ids.md).

### `profile` and `characteristic`

```xml
<profile id="..." name="Warriors" hidden="false"
         typeId="0a0f-00cd-0261-c0ea" typeName="Model">
  <characteristics>
    <characteristic name="M" typeId="da3c-fb2b-4c5f-a22b">3</characteristic>
    ... WS BS S T W I A Ld, in that order ...
  </characteristics>
</profile>
```

There is exactly one profile type in this game system (`Model`). All nine
characteristics should be present, in the game system's order, with `name` matching
the `typeId`.

### `cost`

```xml
<costs><cost name="pts" typeId="eaa7-6800-e651-8bea" value="7.0"/></costs>
```

One cost type only: `pts`. Values are written as floats (`7.0`, `0.0`).

### `constraint`

```xml
<constraint field="selections" scope="parent" value="1.0" percentValue="false"
            shared="true" includeChildSelections="false" includeChildForces="false"
            id="7815-34bf-7554-29ce" type="max"/>
```

* `field` — `selections`, or a cost type id to cap points (`field="eaa7-..."` with
  `scope="parent"` is the magic-item allowance).
* `scope` — `parent`, `roster`, `force`, `self`, or an entry/category id.
* `type` — `min` or `max`.
* `includeChildSelections` — count nested selections too; needed when the thing
  being counted sits inside a group rather than directly under the scope.

### `modifier`

```xml
<modifier type="set" field="hidden" value="true">
  <conditions>
    <condition field="selections" scope="parent" value="1.0" percentValue="false"
               shared="true" includeChildSelections="false" includeChildForces="false"
               childId="4a2b-c497-93f2-c804" type="equalTo"/>
  </conditions>
</modifier>
```

* `type` — `set`, `increment`, `decrement`, `append`, `add`, `remove`,
  `set-primary`, `unset-primary`. `add`/`remove` take a category id in `value`
  and `field="category"`.
* `field` — `hidden`, `name`, `description`, `category`, a cost type id (change the
  price), a characteristic type id (change a stat), or a `constraint/@id`
  (change a limit).
* `conditions` are ANDed. Use `conditionGroups` with `type="and"`/`"or"` for
  anything more involved; they nest.
* `repeats` applies the modifier once per N of something — the idiom for
  per-model upgrade costs.

### `condition`

* `field` — `selections`, or `limit::<costTypeId>` to test the roster points limit.
* `scope` — `parent`, `roster`, `force`, `self`, `ancestor`, `primary-catalogue`,
  or an entry/category id.
* `childId` — what to count: an entry or category id, or the keyword `model`
  (`unit`, `upgrade` also exist). With `scope="primary-catalogue"` and
  `instanceOf`, `childId` is a **catalogue id** — that is the "is this a Bretonnian
  army?" test.
* `type` — `equalTo`, `notEqualTo`, `atLeast`, `atMost`, `greaterThan`, `lessThan`,
  `instanceOf`, `notInstanceOf`.

### `catalogueLink`

```xml
<catalogueLinks>
  <catalogueLink id="..." name="Dogs of War" targetId="3604-800a-4012-5da6"
                 type="catalogue" importRootEntries="true"/>
</catalogueLinks>
```

`importRootEntries="true"` pulls the linked catalogue's top-level entries into this
army list — how mercenaries are shared. It also merges the two id namespaces, so
ids must not collide between them.

## Deploy packaging

`Deploy/<Name>.catz` is a plain zip holding exactly one member, `<Name>.cat`.
`Deploy/index.bsi` is a zip holding `index.xml`. The packaged copies differ from the
root files in three ways, all applied by `scripts/build_deploy.py`:

1. LF line endings instead of CRLF.
2. `catalogue/@gameSystemRevision` refreshed to the `.gst`'s current `revision`.
3. Empty `<description/>` elements dropped, and any element left childless
   collapsed to a self-closing tag.
