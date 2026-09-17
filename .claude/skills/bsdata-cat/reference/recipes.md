# Editing recipes

Copy-paste patterns lifted from this repo. Every `id="..."` shown as `NEW-ID` needs
a fresh value from `scripts/new_id.py`. Ids shown in full are real game system ids
from [gamesystem-ids.md](gamesystem-ids.md) and should be used verbatim.

Attribute boilerplate on `constraint`/`condition`/`repeat`
(`percentValue="false" shared="true" includeChildSelections="..." includeChildForces="false"`)
is mandatory — BattleScribe writes all of it, so keep it even where it looks inert.

---

## A character (Lord / Hero)

`type="model"`, a `Characters` category link plus a primary `Lords` or `Heroes` link,
a profile, then links to the shared `General` entry and the army's Magic Items group.

```xml
<selectionEntry id="NEW-ID" name="Runelord" hidden="false" collective="false" import="true" type="model">
  <constraints>
    <constraint field="selections" scope="roster" value="1.0" percentValue="false" shared="true" includeChildSelections="false" includeChildForces="false" id="NEW-ID" type="max"/>
  </constraints>
  <profiles>
    <profile id="NEW-ID" name="Runelord" hidden="false" typeId="0a0f-00cd-0261-c0ea" typeName="Model">
      <characteristics>
        <characteristic name="M" typeId="da3c-fb2b-4c5f-a22b">3</characteristic>
        <characteristic name="WS" typeId="d46f-1ae5-387f-4ac3">6</characteristic>
        <characteristic name="BS" typeId="22c7-799b-e07c-f32c">4</characteristic>
        <characteristic name="S" typeId="0c58-1252-962d-8fcc">4</characteristic>
        <characteristic name="T" typeId="16d7-9f22-06d8-8427">5</characteristic>
        <characteristic name="W" typeId="f9d0-a5b0-7e0b-a404">3</characteristic>
        <characteristic name="I" typeId="b418-0e30-644f-1435">3</characteristic>
        <characteristic name="A" typeId="fa03-f9a3-8117-98dd">3</characteristic>
        <characteristic name="Ld" typeId="bbad-d421-400b-87c1">10</characteristic>
      </characteristics>
    </profile>
  </profiles>
  <categoryLinks>
    <categoryLink id="NEW-ID" name="Characters" hidden="false" targetId="48f1-4778-a9db-cde7" primary="false"/>
    <categoryLink id="NEW-ID" name="Lords" hidden="false" targetId="623e-5f3d-d939-9b51" primary="true"/>
  </categoryLinks>
  <entryLinks>
    <entryLink id="NEW-ID" name="Magic Items" hidden="false" collective="false" import="true" targetId="ARMY-MAGIC-ITEMS-GROUP-ID" type="selectionEntryGroup"/>
    <entryLink id="NEW-ID" name="General" hidden="false" collective="false" import="true" targetId="cf7b-798c-9b94-df74" type="selectionEntry"/>
  </entryLinks>
  <costs>
    <cost name="pts" typeId="eaa7-6800-e651-8bea" value="140.0"/>
  </costs>
</selectionEntry>
```

A wizard also takes the `Wizard` category (`eb46-88d4-eb41-2549`) and links to
`Wizard Level (Lord)` `afae-7702-64a2-3f42` or `Wizard Level (Hero)`
`ed43-1e9a-5409-abc6`, plus `Lore of Magic` `3c79-613e-77df-160c` — or an
army-specific lore group where the choice is restricted.

Find the army's own Magic Items group id with:

```bash
python .claude/skills/bsdata-cat/scripts/find_id.py --in "Dwarfs.cat" "Magic Items" --tag selectionEntryGroup
```

## A rank-and-file unit

`type="unit"` wrapping a `type="model"` child. The **unit** entry costs 0 pts and
carries the category; the **model** child carries the per-model cost and the
minimum unit size.

```xml
<selectionEntry id="NEW-ID" name="Dwarf Warriors" hidden="false" collective="false" import="true" type="unit">
  <categoryLinks>
    <categoryLink id="NEW-ID" name="Core" hidden="false" targetId="62d3-efc6-6c2c-634e" primary="true"/>
  </categoryLinks>
  <selectionEntries>
    <selectionEntry id="NEW-ID" name="Warriors" hidden="false" collective="false" import="true" type="model">
      <constraints>
        <constraint field="selections" scope="parent" value="10.0" percentValue="false" shared="true" includeChildSelections="false" includeChildForces="false" id="NEW-ID" type="min"/>
      </constraints>
      <profiles>...</profiles>
      <costs><cost name="pts" typeId="eaa7-6800-e651-8bea" value="7.0"/></costs>
    </selectionEntry>
  </selectionEntries>
  <selectionEntryGroups>
    <selectionEntryGroup id="NEW-ID" name="Command" hidden="false" collective="false" import="true">
      <selectionEntries>
        <!-- Musician / Standard Bearer / Champion, each max 1, flat cost -->
      </selectionEntries>
    </selectionEntryGroup>
  </selectionEntryGroups>
  <costs><cost name="pts" typeId="eaa7-6800-e651-8bea" value="0.0"/></costs>
</selectionEntry>
```

Add a unit-size cap with a second constraint on the model, `type="max"`.

## A unit-wide upgrade priced per model

The upgrade itself costs 0; a `repeat` on the models adds the per-model price.
This is "+1 pt/model for shields".

```xml
<selectionEntry id="NEW-ID" name="Shields" hidden="false" collective="false" import="true" type="upgrade">
  <modifiers>
    <modifier type="increment" field="eaa7-6800-e651-8bea" value="1.0">
      <repeats>
        <repeat field="selections" scope="parent" value="1.0" percentValue="false" shared="true" includeChildSelections="false" includeChildForces="false" childId="model" repeats="1" roundUp="false"/>
      </repeats>
    </modifier>
  </modifiers>
  <constraints>
    <constraint field="selections" scope="parent" value="1.0" percentValue="false" shared="true" includeChildSelections="false" includeChildForces="false" id="NEW-ID" type="max"/>
  </constraints>
  <costs><cost name="pts" typeId="eaa7-6800-e651-8bea" value="0.0"/></costs>
</selectionEntry>
```

`childId="model"` counts every model in the parent unit, whatever it is called.

## Mutually exclusive options

Wrap them in a group and cap the group at 1. Add a `min` of 1 to force a choice,
and `defaultSelectionEntryId` to preselect one.

```xml
<selectionEntryGroup id="NEW-ID" name="Armour" hidden="false" collective="false" import="true" defaultSelectionEntryId="LIGHT-ARMOUR-ID">
  <constraints>
    <constraint field="selections" scope="parent" value="1.0" percentValue="false" shared="true" includeChildSelections="false" includeChildForces="false" id="NEW-ID" type="max"/>
    <constraint field="selections" scope="parent" value="1.0" percentValue="false" shared="true" includeChildSelections="false" includeChildForces="false" id="NEW-ID" type="min"/>
  </constraints>
  <selectionEntries>...</selectionEntries>
</selectionEntryGroup>
```

For options in *different* groups (a mundane shield vs a magic shield), zero out the
one when the other is taken by pointing a modifier at the loser's max constraint:

```xml
<modifiers>
  <modifier type="set" field="THE-MAX-CONSTRAINT-ID" value="0.0">
    <conditions>
      <condition field="selections" scope="parent" value="1.0" percentValue="false" shared="true" includeChildSelections="false" includeChildForces="false" childId="4a2b-c497-93f2-c804" type="equalTo"/>
    </conditions>
  </modifier>
</modifiers>
```

## Hide a whole branch unless something is true

Wizard-only arcane items, banner-only magic banners. Put the modifier on the
`entryLink`, not the target.

```xml
<entryLink id="NEW-ID" name="Arcane Items" hidden="false" collective="false" import="true" targetId="..." type="selectionEntryGroup">
  <modifiers>
    <modifier type="set" field="hidden" value="true">
      <conditions>
        <condition field="selections" scope="parent" value="0.0" percentValue="false" shared="true" includeChildSelections="false" includeChildForces="false" childId="eb46-88d4-eb41-2549" type="notInstanceOf"/>
      </conditions>
    </modifier>
  </modifiers>
</entryLink>
```

`instanceOf` / `notInstanceOf` with a **category** id in `childId` tests "does the
scope belong to this category?". With `scope="primary-catalogue"` and a **catalogue**
id it tests which army book the roster is using.

## Magic item allowance

A points cap on the Magic Items group, raised for Lords:

```xml
<selectionEntryGroup id="NEW-ID" name="Magic Items" hidden="false" collective="false" import="true">
  <modifiers>
    <modifier type="set" field="THE-CONSTRAINT-ID" value="100.0">
      <conditions>
        <condition field="selections" scope="parent" value="0.0" percentValue="false" shared="true" includeChildSelections="false" includeChildForces="false" childId="623e-5f3d-d939-9b51" type="instanceOf"/>
      </conditions>
    </modifier>
  </modifiers>
  <constraints>
    <constraint field="eaa7-6800-e651-8bea" scope="parent" value="50.0" percentValue="false" shared="true" includeChildSelections="false" includeChildForces="false" id="THE-CONSTRAINT-ID" type="max"/>
  </constraints>
  <entryLinks>
    <!-- Magic Weapons / Magic Armour / Talismans / Enchanted Items / Magic Banners / Arcane Items -->
  </entryLinks>
</selectionEntryGroup>
```

## A magic item

An army-specific item is a `type="upgrade"` entry inside the relevant category
group, with a roster-wide `max 1` (items are unique), a parent `max 1`, its rule
text, and its item-category links.

```xml
<selectionEntry id="NEW-ID" name="Rune of Spellbreaking" hidden="false" collective="false" import="true" type="upgrade">
  <constraints>
    <constraint field="selections" scope="roster" value="1.0" percentValue="false" shared="true" includeChildSelections="true" includeChildForces="false" id="NEW-ID" type="max"/>
    <constraint field="selections" scope="parent" value="1.0" percentValue="false" shared="true" includeChildSelections="true" includeChildForces="false" id="NEW-ID" type="max"/>
  </constraints>
  <rules>
    <rule id="NEW-ID" name="Rune of Spellbreaking" hidden="false">
      <description>One use only. Automatically dispel an enemy spell.</description>
    </rule>
  </rules>
  <categoryLinks>
    <categoryLink id="NEW-ID" name="Arcane Item" hidden="false" targetId="7cfd-b676-48e1-6eec" primary="true"/>
  </categoryLinks>
  <costs><cost name="pts" typeId="eaa7-6800-e651-8bea" value="25.0"/></costs>
</selectionEntry>
```

To offer one of the **common** magic items from the `.gst`, link it instead of
copying it — see the shared entry ids in [gamesystem-ids.md](gamesystem-ids.md):

```xml
<entryLink id="NEW-ID" name="Dispel Scroll" hidden="false" collective="false" import="true" targetId="52c3-25b3-e386-3449" type="selectionEntry"/>
```

Put a re-price or an extra category on the link, not on the shared target — the
target is shared by every army.

## 0–1 per army, and N per 1000 points

Per army: `scope="roster"`, `type="max"`, `value="1.0"`.

Scaling with game size uses `repeats` on the roster points limit:

```xml
<modifier type="increment" field="THE-MAX-CONSTRAINT-ID" value="1.0">
  <repeats>
    <repeat field="limit::eaa7-6800-e651-8bea" scope="roster" value="1000.0" percentValue="false" shared="true" includeChildSelections="true" includeChildForces="false" childId="model" repeats="1" roundUp="false"/>
  </repeats>
</modifier>
```

## Moving an entry between force-org slots

Categories are added and removed as a set, and the primary flag has to move with
them. Wrap the lot in a `modifierGroup` with a `<comment>` explaining the rule —
this repo does exactly that for Lizardmen Sacred Spawnings.

```xml
<modifierGroups>
  <modifierGroup>
    <comment>Set category to Rare if 2 Sacred Spawnings</comment>
    <conditionGroups>
      <conditionGroup type="and">
        <conditions>...</conditions>
      </conditionGroup>
    </conditionGroups>
    <modifiers>
      <modifier type="remove" field="category" value="62d3-efc6-6c2c-634e"/>
      <modifier type="add" field="category" value="a3af-995e-0cf1-7091"/>
      <modifier type="unset-primary" field="category" value="62d3-efc6-6c2c-634e"/>
      <modifier type="set-primary" field="category" value="a3af-995e-0cf1-7091"/>
    </modifiers>
  </modifierGroup>
</modifierGroups>
```

## Attaching a special rule

Army-specific text goes in a local `<rules>` block. Anything in the `.gst`'s
`sharedRules` (Fear, Terror, Fly, Skirmishers, Killing Blow, …) is referenced by
`infoLink` so the text stays in one place:

```xml
<infoLinks>
  <infoLink id="NEW-ID" name="Fear" hidden="false" targetId="03be-3e56-1332-bf56" type="rule"/>
</infoLinks>
```

Rules used by several entries in the same army belong in that catalogue's
`<sharedRules>`, linked the same way.

## Changing a points cost

Edit the `<cost value="...">` on the entry. If the entry is a shared one in the
`.gst`, changing it changes it for every army — check with
`find_id.py <id>` who links to it first. If only one army should differ, override
on that army's `entryLink` with a `modifier type="set" field="eaa7-6800-e651-8bea"`.
