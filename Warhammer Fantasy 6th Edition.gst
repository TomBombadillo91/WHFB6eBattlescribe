<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<gameSystem id="4ca8-2035-2f87-1bd7" name="WHFB 6th Edition" revision="34" battleScribeVersion="2.03" authorName="Tom Clare" authorContact="" authorUrl="" xmlns="http://www.battlescribe.net/schema/gameSystemSchema">
  <publications>
    <publication id="d9e7-add3-773e-ffab" name="BRB"/>
    <publication id="2c29-8521-dcc7-5337" name="Warhammer Chronicles 2003"/>
    <publication id="c2a3-b0b2-12f3-4d2f" name="Storm of Chaos"/>
  </publications>
  <costTypes>
    <costType id="eaa7-6800-e651-8bea" name="pts" defaultCostLimit="-1.0" hidden="false"/>
  </costTypes>
  <profileTypes>
    <profileType id="0a0f-00cd-0261-c0ea" name="Model">
      <characteristicTypes>
        <characteristicType id="da3c-fb2b-4c5f-a22b" name="M"/>
        <characteristicType id="d46f-1ae5-387f-4ac3" name="WS"/>
        <characteristicType id="22c7-799b-e07c-f32c" name="BS"/>
        <characteristicType id="0c58-1252-962d-8fcc" name="S"/>
        <characteristicType id="16d7-9f22-06d8-8427" name="T"/>
        <characteristicType id="f9d0-a5b0-7e0b-a404" name="W"/>
        <characteristicType id="b418-0e30-644f-1435" name="I"/>
        <characteristicType id="fa03-f9a3-8117-98dd" name="A"/>
        <characteristicType id="bbad-d421-400b-87c1" name="Ld"/>
      </characteristicTypes>
    </profileType>
  </profileTypes>
  <categoryEntries>
    <categoryEntry id="62d3-efc6-6c2c-634e" name="Core" hidden="false"/>
    <categoryEntry id="623e-5f3d-d939-9b51" name="Lords" hidden="false"/>
    <categoryEntry id="4a3f-84d1-0495-6ecb" name="Special" hidden="false"/>
    <categoryEntry id="a3af-995e-0cf1-7091" name="Rare" hidden="false"/>
    <categoryEntry id="48f1-4778-a9db-cde7" name="Characters" hidden="false"/>
    <categoryEntry id="5694-61f3-6913-6154" name="Heroes" hidden="false"/>
    <categoryEntry id="e6e5-cff5-9987-d563" name="Magic Weapon" hidden="false"/>
    <categoryEntry id="2963-aff1-28ca-7634" name="Magic Armour" hidden="false"/>
    <categoryEntry id="7cfd-b676-48e1-6eec" name="Arcane Item" hidden="false"/>
    <categoryEntry id="06f3-5988-1d55-db7c" name="Scroll" hidden="false"/>
    <categoryEntry id="d777-f2f1-e0db-8e8e" name="Talisman" hidden="false"/>
    <categoryEntry id="daeb-6ab0-83b2-8bf3" name="Magic Banner" hidden="false"/>
    <categoryEntry id="d8eb-f296-d241-3c6d" name="Enchanted Item" hidden="false"/>
    <categoryEntry id="eb46-88d4-eb41-2549" name="Wizard" hidden="false"/>
    <categoryEntry id="1a61-9b9e-0b56-e6ce" name="General" hidden="false"/>
    <categoryEntry id="4c58-0153-f37e-9905" name="Magic Shield" hidden="false"/>
    <categoryEntry id="4e99-ada4-8f3b-ed30" name="Additional Hero Choice" hidden="true"/>
    <categoryEntry id="fcd6-2f77-ca6e-7b24" name="Chariot" hidden="false">
      <infoLinks>
        <infoLink id="be5e-b2e5-9cda-69f1" name="Chariot" hidden="false" targetId="4bb1-dfab-2824-bad1" type="rule"/>
      </infoLinks>
    </categoryEntry>
    <categoryEntry id="8a03-13c0-ea45-1732" name="Ignored for min Core" hidden="false"/>
    <categoryEntry id="de79-e832-4f30-ac18" name="Mount" hidden="false"/>
    <categoryEntry id="b91d-d3b1-8b46-6d52" name="Special Character" hidden="false"/>
    <categoryEntry id="fedc-da5a-410d-84bd" name="Bound Spell Item" hidden="false">
      <constraints>
        <constraint field="selections" scope="parent" value="1.0" percentValue="false" shared="true" includeChildSelections="true" includeChildForces="false" id="bf1d-6d71-81aa-e3ca" type="max"/>
      </constraints>
    </categoryEntry>
    <categoryEntry id="0daf-8d53-eadf-d10f" name="Additional Lord Choice" hidden="true"/>
    <categoryEntry id="9236-407c-ba73-9b10" name="Grants Extra Rare Choice" hidden="false"/>
    <categoryEntry id="1c0b-2b0f-459f-d6f9" name="Additional Rare Choice" hidden="true"/>
    <categoryEntry id="9dc5-bbce-5738-84e8" name="Two Additional Hero Choices" hidden="true"/>
    <categoryEntry id="182a-f76f-634c-e9be" name="Non-Scroll Arcane Item" hidden="true"/>
  </categoryEntries>
  <forceEntries>
    <forceEntry id="5f75-906f-4d23-7a30" name="Warhammer Fantasy 6th Edition" hidden="false">
      <categoryLinks>
        <categoryLink id="8472-9fb7-4f93-8c2b" name="Lords" hidden="false" targetId="623e-5f3d-d939-9b51" primary="false">
          <modifiers>
            <modifier type="decrement" field="4ca5-3015-2631-2b7d" value="1.0">
              <repeats>
                <repeat field="selections" scope="parent" value="1.0" percentValue="false" shared="true" includeChildSelections="false" includeChildForces="false" childId="0daf-8d53-eadf-d10f" repeats="1" roundUp="false"/>
              </repeats>
              <conditions>
                <condition field="limit::eaa7-6800-e651-8bea" scope="roster" value="1999.0" percentValue="false" shared="true" includeChildSelections="true" includeChildForces="true" childId="0daf-8d53-eadf-d10f" type="greaterThan"/>
              </conditions>
            </modifier>
          </modifiers>
          <modifierGroups>
            <modifierGroup>
              <modifiers>
                <modifier type="set" field="4ca5-3015-2631-2b7d" value="0.0">
                  <conditions>
                    <condition field="limit::eaa7-6800-e651-8bea" scope="roster" value="2000.0" percentValue="false" shared="true" includeChildSelections="false" includeChildForces="false" childId="model" type="lessThan"/>
                  </conditions>
                </modifier>
                <modifier type="increment" field="4ca5-3015-2631-2b7d" value="1.0">
                  <repeats>
                    <repeat field="limit::eaa7-6800-e651-8bea" scope="roster" value="1000.0" percentValue="false" shared="true" includeChildSelections="true" includeChildForces="false" childId="model" repeats="1" roundUp="false"/>
                  </repeats>
                  <conditions>
                    <condition field="limit::eaa7-6800-e651-8bea" scope="roster" value="1999.0" percentValue="false" shared="true" includeChildSelections="true" includeChildForces="false" childId="model" type="greaterThan"/>
                  </conditions>
                </modifier>
              </modifiers>
            </modifierGroup>
          </modifierGroups>
          <constraints>
            <constraint field="selections" scope="parent" value="-1.0" percentValue="false" shared="true" includeChildSelections="true" includeChildForces="false" id="4ca5-3015-2631-2b7d" type="max"/>
          </constraints>
        </categoryLink>
        <categoryLink id="67cc-8ba2-0da1-f486" name="Heroes" hidden="false" targetId="5694-61f3-6913-6154" primary="false">
          <modifiers>
            <modifier type="set" field="75f4-2d2a-d6a1-e901" value="4.0">
              <conditionGroups>
                <conditionGroup type="and">
                  <conditions>
                    <condition field="limit::eaa7-6800-e651-8bea" scope="roster" value="3000.0" percentValue="false" shared="true" includeChildSelections="true" includeChildForces="false" childId="model" type="lessThan"/>
                    <condition field="limit::eaa7-6800-e651-8bea" scope="roster" value="1999.0" percentValue="false" shared="true" includeChildSelections="false" includeChildForces="false" childId="model" type="greaterThan"/>
                  </conditions>
                </conditionGroup>
              </conditionGroups>
            </modifier>
            <modifier type="set" field="75f4-2d2a-d6a1-e901" value="3.0">
              <conditions>
                <condition field="limit::eaa7-6800-e651-8bea" scope="roster" value="2000.0" percentValue="false" shared="true" includeChildSelections="true" includeChildForces="false" childId="model" type="lessThan"/>
              </conditions>
            </modifier>
            <modifier type="set" field="75f4-2d2a-d6a1-e901" value="0.0">
              <conditions>
                <condition field="limit::eaa7-6800-e651-8bea" scope="roster" value="2999.0" percentValue="false" shared="true" includeChildSelections="true" includeChildForces="false" childId="model" type="greaterThan"/>
              </conditions>
            </modifier>
            <modifier type="increment" field="75f4-2d2a-d6a1-e901" value="2.0">
              <repeats>
                <repeat field="limit::eaa7-6800-e651-8bea" scope="roster" value="1000.0" percentValue="false" shared="true" includeChildSelections="false" includeChildForces="false" childId="model" repeats="1" roundUp="false"/>
              </repeats>
              <conditions>
                <condition field="limit::eaa7-6800-e651-8bea" scope="roster" value="2999.0" percentValue="false" shared="true" includeChildSelections="true" includeChildForces="false" childId="model" type="greaterThan"/>
              </conditions>
            </modifier>
            <modifier type="decrement" field="75f4-2d2a-d6a1-e901" value="1.0">
              <repeats>
                <repeat field="selections" scope="roster" value="1.0" percentValue="false" shared="true" includeChildSelections="false" includeChildForces="true" childId="4e99-ada4-8f3b-ed30" repeats="1" roundUp="false"/>
              </repeats>
            </modifier>
            <modifier type="increment" field="75f4-2d2a-d6a1-e901" value="1.0">
              <conditions>
                <condition field="selections" scope="primary-catalogue" value="0.0" percentValue="false" shared="true" includeChildSelections="false" includeChildForces="false" childId="05b9-5022-67cd-4fd3" type="instanceOf"/>
              </conditions>
            </modifier>
            <modifier type="decrement" field="75f4-2d2a-d6a1-e901" value="2.0">
              <repeats>
                <repeat field="selections" scope="roster" value="1.0" percentValue="false" shared="true" includeChildSelections="true" includeChildForces="true" childId="9dc5-bbce-5738-84e8" repeats="1" roundUp="false"/>
              </repeats>
            </modifier>
          </modifiers>
          <constraints>
            <constraint field="selections" scope="parent" value="-1.0" percentValue="false" shared="true" includeChildSelections="true" includeChildForces="false" id="75f4-2d2a-d6a1-e901" type="max"/>
          </constraints>
        </categoryLink>
        <categoryLink id="f2d7-f8a2-7e14-ef5e" name="Core" hidden="false" targetId="62d3-efc6-6c2c-634e" primary="false">
          <modifiers>
            <modifier type="decrement" field="98ab-f7f1-5fb5-18c3" value="1.0">
              <conditions>
                <condition field="limit::eaa7-6800-e651-8bea" scope="roster" value="1999.0" percentValue="false" shared="true" includeChildSelections="true" includeChildForces="true" childId="model" type="greaterThan"/>
              </conditions>
            </modifier>
            <modifier type="increment" field="98ab-f7f1-5fb5-18c3" value="1.0">
              <repeats>
                <repeat field="limit::eaa7-6800-e651-8bea" scope="roster" value="1000.0" percentValue="false" shared="true" includeChildSelections="true" includeChildForces="false" childId="model" repeats="1" roundUp="false"/>
              </repeats>
              <conditions>
                <condition field="limit::eaa7-6800-e651-8bea" scope="roster" value="1999.0" percentValue="false" shared="true" includeChildSelections="true" includeChildForces="false" childId="model" type="greaterThan"/>
              </conditions>
            </modifier>
            <modifier type="increment" field="98ab-f7f1-5fb5-18c3" value="1.0">
              <repeats>
                <repeat field="selections" scope="parent" value="1.0" percentValue="false" shared="true" includeChildSelections="false" includeChildForces="false" childId="8a03-13c0-ea45-1732" repeats="1" roundUp="false"/>
              </repeats>
            </modifier>
          </modifiers>
          <constraints>
            <constraint field="selections" scope="force" value="2.0" percentValue="false" shared="true" includeChildSelections="true" includeChildForces="true" id="98ab-f7f1-5fb5-18c3" type="min"/>
          </constraints>
        </categoryLink>
        <categoryLink id="abaa-abc3-5162-6a22" name="Special" hidden="false" targetId="4a3f-84d1-0495-6ecb" primary="false">
          <modifiers>
            <modifier type="set" field="f140-733f-991c-4d18" value="3.0">
              <conditions>
                <condition field="limit::eaa7-6800-e651-8bea" scope="roster" value="2000.0" percentValue="false" shared="true" includeChildSelections="false" includeChildForces="false" childId="model" type="lessThan"/>
              </conditions>
            </modifier>
          </modifiers>
          <modifierGroups>
            <modifierGroup>
              <modifiers>
                <modifier type="set" field="f140-733f-991c-4d18" value="2.0">
                  <conditions>
                    <condition field="limit::eaa7-6800-e651-8bea" scope="roster" value="1999.0" percentValue="false" shared="true" includeChildSelections="false" includeChildForces="false" childId="model" type="greaterThan"/>
                  </conditions>
                </modifier>
                <modifier type="increment" field="f140-733f-991c-4d18" value="1.0">
                  <repeats>
                    <repeat field="limit::eaa7-6800-e651-8bea" scope="roster" value="1000.0" percentValue="false" shared="true" includeChildSelections="false" includeChildForces="false" childId="model" repeats="1" roundUp="false"/>
                  </repeats>
                  <conditions>
                    <condition field="limit::eaa7-6800-e651-8bea" scope="roster" value="1999.0" percentValue="false" shared="true" includeChildSelections="false" includeChildForces="false" childId="model" type="greaterThan"/>
                  </conditions>
                </modifier>
              </modifiers>
            </modifierGroup>
          </modifierGroups>
          <constraints>
            <constraint field="selections" scope="parent" value="-1.0" percentValue="false" shared="true" includeChildSelections="false" includeChildForces="false" id="f140-733f-991c-4d18" type="max"/>
          </constraints>
        </categoryLink>
        <categoryLink id="b6e8-eda4-372a-43dd" name="Rare" hidden="false" targetId="a3af-995e-0cf1-7091" primary="false">
          <modifiers>
            <modifier type="set" field="abcb-d080-e34a-9d53" value="1.0">
              <conditions>
                <condition field="limit::eaa7-6800-e651-8bea" scope="roster" value="2000.0" percentValue="false" shared="true" includeChildSelections="false" includeChildForces="false" childId="model" type="lessThan"/>
              </conditions>
            </modifier>
            <modifier type="increment" field="abcb-d080-e34a-9d53" value="1.0">
              <repeats>
                <repeat field="selections" scope="roster" value="1.0" percentValue="false" shared="true" includeChildSelections="true" includeChildForces="true" childId="9236-407c-ba73-9b10" repeats="1" roundUp="false"/>
              </repeats>
            </modifier>
            <modifier type="decrement" field="abcb-d080-e34a-9d53" value="1.0">
              <repeats>
                <repeat field="selections" scope="roster" value="1.0" percentValue="false" shared="true" includeChildSelections="true" includeChildForces="true" childId="1c0b-2b0f-459f-d6f9" repeats="1" roundUp="false"/>
              </repeats>
            </modifier>
          </modifiers>
          <modifierGroups>
            <modifierGroup>
              <conditions>
                <condition field="limit::eaa7-6800-e651-8bea" scope="roster" value="1999.0" percentValue="false" shared="true" includeChildSelections="false" includeChildForces="false" childId="model" type="greaterThan"/>
              </conditions>
              <modifiers>
                <modifier type="decrement" field="abcb-d080-e34a-9d53" value="1.0"/>
                <modifier type="increment" field="abcb-d080-e34a-9d53" value="1.0">
                  <repeats>
                    <repeat field="limit::eaa7-6800-e651-8bea" scope="roster" value="1000.0" percentValue="false" shared="true" includeChildSelections="false" includeChildForces="false" childId="model" repeats="1" roundUp="false"/>
                  </repeats>
                </modifier>
              </modifiers>
            </modifierGroup>
          </modifierGroups>
          <constraints>
            <constraint field="selections" scope="parent" value="1.0" percentValue="false" shared="true" includeChildSelections="true" includeChildForces="true" id="abcb-d080-e34a-9d53" type="max"/>
          </constraints>
        </categoryLink>
        <categoryLink id="1821-b8e0-2aa1-b805" name="Characters" hidden="false" targetId="48f1-4778-a9db-cde7" primary="false">
          <modifiers>
            <modifier type="set" field="562f-9770-dc82-1b05" value="4.0">
              <conditionGroups>
                <conditionGroup type="and">
                  <conditions>
                    <condition field="limit::eaa7-6800-e651-8bea" scope="roster" value="3000.0" percentValue="false" shared="true" includeChildSelections="true" includeChildForces="false" childId="model" type="lessThan"/>
                    <condition field="limit::eaa7-6800-e651-8bea" scope="roster" value="1999.0" percentValue="false" shared="true" includeChildSelections="false" includeChildForces="false" childId="model" type="greaterThan"/>
                  </conditions>
                </conditionGroup>
              </conditionGroups>
            </modifier>
            <modifier type="set" field="562f-9770-dc82-1b05" value="3.0">
              <conditions>
                <condition field="limit::eaa7-6800-e651-8bea" scope="roster" value="2000.0" percentValue="false" shared="true" includeChildSelections="true" includeChildForces="false" childId="model" type="lessThan"/>
              </conditions>
            </modifier>
            <modifier type="set" field="562f-9770-dc82-1b05" value="0.0">
              <conditions>
                <condition field="limit::eaa7-6800-e651-8bea" scope="roster" value="2999.0" percentValue="false" shared="true" includeChildSelections="true" includeChildForces="false" childId="model" type="greaterThan"/>
              </conditions>
            </modifier>
            <modifier type="increment" field="562f-9770-dc82-1b05" value="2.0">
              <repeats>
                <repeat field="limit::eaa7-6800-e651-8bea" scope="roster" value="1000.0" percentValue="false" shared="true" includeChildSelections="false" includeChildForces="false" childId="model" repeats="1" roundUp="false"/>
              </repeats>
              <conditions>
                <condition field="limit::eaa7-6800-e651-8bea" scope="roster" value="2999.0" percentValue="false" shared="true" includeChildSelections="true" includeChildForces="false" childId="model" type="greaterThan"/>
              </conditions>
            </modifier>
            <modifier type="increment" field="562f-9770-dc82-1b05" value="1.0">
              <conditions>
                <condition field="selections" scope="primary-catalogue" value="0.0" percentValue="false" shared="true" includeChildSelections="false" includeChildForces="false" childId="05b9-5022-67cd-4fd3" type="instanceOf"/>
              </conditions>
            </modifier>
            <modifier type="decrement" field="562f-9770-dc82-1b05" value="1.0">
              <repeats>
                <repeat field="selections" scope="roster" value="1.0" percentValue="false" shared="true" includeChildSelections="false" includeChildForces="true" childId="4e99-ada4-8f3b-ed30" repeats="1" roundUp="false"/>
              </repeats>
            </modifier>
            <modifier type="decrement" field="562f-9770-dc82-1b05" value="2.0">
              <repeats>
                <repeat field="selections" scope="roster" value="1.0" percentValue="false" shared="true" includeChildSelections="false" includeChildForces="true" childId="9dc5-bbce-5738-84e8" repeats="1" roundUp="false"/>
              </repeats>
            </modifier>
          </modifiers>
          <constraints>
            <constraint field="selections" scope="parent" value="-1.0" percentValue="false" shared="true" includeChildSelections="true" includeChildForces="false" id="562f-9770-dc82-1b05" type="max"/>
          </constraints>
        </categoryLink>
      </categoryLinks>
    </forceEntry>
  </forceEntries>
  <sharedSelectionEntries>
    <selectionEntry id="52c3-25b3-e386-3449" name="Dispel Scroll" publicationId="d9e7-add3-773e-ffab" hidden="false" collective="false" import="true" type="upgrade">
      <rules>
        <rule id="5e03-7f49-bf00-ae05" name="Dispel Scroll" hidden="false">
          <description>A Dispel Scroll is inscribed with a powerful anti-magical invocation. When it is read out by a Wizard, the effect is to drain away magical power and weaken a spell that has been cast. As soon as a spell has been cast, any Wizard who has a Dispel Scroll can read it. This automatically dispels the cast spell, no dice roll is required.

Reading a Dispel Scroll will bring any spell cast by the Wizard reading it to an end. To put it another way, a Wizard who has a spell in play will automatically cancel it by reading a Dispel Scroll.

As with all scrolls, Dispel Scrolls are not unique items - they are prepared by a Wizard prior to battle and it is quite possible for several Wizards to carry Dispel Scrolls, and for a Wizard to carry more than one. However, only one can be used at a time.

Note that a Dispel Scroll will not help if the spell has been cast with Irresistible Force. Any spell that is successfully cast with two or more 6s is Irresistible and no Dispel roll is permitted.</description>
        </rule>
      </rules>
      <categoryLinks>
        <categoryLink id="9146-8e81-39ba-680f" name="Scroll" hidden="false" targetId="06f3-5988-1d55-db7c" primary="false"/>
        <categoryLink id="290a-7302-5c44-1f61" name="New CategoryLink" hidden="false" targetId="7cfd-b676-48e1-6eec" primary="true"/>
      </categoryLinks>
      <costs>
        <cost name="pts" typeId="eaa7-6800-e651-8bea" value="25.0"/>
      </costs>
    </selectionEntry>
    <selectionEntry id="0871-b449-88b1-0a33" name="Staff of Sorcery" publicationId="d9e7-add3-773e-ffab" hidden="false" collective="false" import="true" type="upgrade">
      <constraints>
        <constraint field="selections" scope="roster" value="1.0" percentValue="false" shared="true" includeChildSelections="true" includeChildForces="false" id="8fa7-8516-0b40-fada" type="max"/>
        <constraint field="selections" scope="parent" value="1.0" percentValue="false" shared="true" includeChildSelections="true" includeChildForces="false" id="7ff1-f364-267b-bc62" type="max"/>
      </constraints>
      <rules>
        <rule id="9fb5-4b85-58e8-39db" name="Staff of Sorcery" hidden="false">
          <description>+1 To Dispel. A Wizard who has this benefits from the arcane power stored within it. Whenever he dispels a spell, the score required to make a successful dispel is reduced by 1.</description>
        </rule>
      </rules>
      <categoryLinks>
        <categoryLink id="b4a3-bb83-6650-8d0e" name="New CategoryLink" hidden="false" targetId="7cfd-b676-48e1-6eec" primary="true"/>
      </categoryLinks>
      <costs>
        <cost name="pts" typeId="eaa7-6800-e651-8bea" value="50.0"/>
      </costs>
    </selectionEntry>
    <selectionEntry id="4a2b-c497-93f2-c804" name="Enchanted Shield" publicationId="d9e7-add3-773e-ffab" hidden="false" collective="false" import="true" type="upgrade">
      <constraints>
        <constraint field="selections" scope="roster" value="1.0" percentValue="false" shared="true" includeChildSelections="true" includeChildForces="false" id="4a1e-0897-cb52-3686" type="max"/>
        <constraint field="selections" scope="parent" value="1.0" percentValue="false" shared="true" includeChildSelections="true" includeChildForces="false" id="b573-d1b1-1c2c-7a16" type="max"/>
      </constraints>
      <rules>
        <rule id="94bc-dc3b-0290-d0a6" name="Enchanted Shield" hidden="false">
          <description>5+ Armour Save. The Enchanted Shield protects its user with powerful magic. The shield confers an armour save of 5+ rather than a mundane shield&apos;s armour save of 6+. This can be combined with other magical or mundane armour - for example, light armour + Enchanted Shield = armour save 4+, heavy armour + Enchanted Shield + mounted = armour save 2+.</description>
        </rule>
      </rules>
      <categoryLinks>
        <categoryLink id="752f-8c3e-3908-833b" name="Shield" hidden="false" targetId="4c58-0153-f37e-9905" primary="true"/>
      </categoryLinks>
      <costs>
        <cost name="pts" typeId="eaa7-6800-e651-8bea" value="10.0"/>
      </costs>
    </selectionEntry>
    <selectionEntry id="862d-4fba-1966-3f2f" name="War Banner" publicationId="d9e7-add3-773e-ffab" hidden="false" collective="false" import="true" type="upgrade">
      <constraints>
        <constraint field="selections" scope="roster" value="1.0" percentValue="false" shared="true" includeChildSelections="true" includeChildForces="false" id="ea28-9209-9761-90bc" type="max"/>
        <constraint field="selections" scope="parent" value="1.0" percentValue="false" shared="true" includeChildSelections="true" includeChildForces="false" id="eb4c-6af2-f0e2-728e" type="max"/>
      </constraints>
      <rules>
        <rule id="9aa2-b4ca-96ef-b222" name="War Banner" hidden="false">
          <description>+1 Combat Resolution. The War Banner carries powerful enchantments that fill all those who fight beneath it with heroic courage and determination. A unit, which has a War Banner adds a further +1. to its combat resolution when working out which side has won the combat.</description>
        </rule>
      </rules>
      <categoryLinks>
        <categoryLink id="15d2-9936-6cb3-6573" name="New CategoryLink" hidden="false" targetId="daeb-6ab0-83b2-8bf3" primary="true"/>
      </categoryLinks>
      <costs>
        <cost name="pts" typeId="eaa7-6800-e651-8bea" value="25.0"/>
      </costs>
    </selectionEntry>
    <selectionEntry id="3c3e-b471-60a2-bcb5" name="Biting Blade" publicationId="d9e7-add3-773e-ffab" hidden="false" collective="false" import="true" type="upgrade">
      <constraints>
        <constraint field="selections" scope="roster" value="1.0" percentValue="false" shared="true" includeChildSelections="true" includeChildForces="false" id="0248-3e59-1759-59f2" type="max"/>
        <constraint field="selections" scope="parent" value="1.0" percentValue="false" shared="true" includeChildSelections="true" includeChildForces="false" id="f261-d569-bd3e-2836" type="max"/>
      </constraints>
      <rules>
        <rule id="108c-01e7-0f28-a87d" name="Biting Blade" hidden="false">
          <description>-1 Armour Save. The Biting Blade is forged with bitter curses that work against the armour of its foes. The blade confers an additional -1 armour save modifier on any blows stuck. This is in addition to any normal armour save modifier for Strength, so a blow struck at Strength 3 or less will have a -1 armour save. a Strength 4 hit has a -2 armour save, Strength 5 has a -3 armour save and so on.</description>
        </rule>
      </rules>
      <categoryLinks>
        <categoryLink id="19f0-79c1-9369-db2d" name="New CategoryLink" hidden="false" targetId="e6e5-cff5-9987-d563" primary="true"/>
      </categoryLinks>
      <costs>
        <cost name="pts" typeId="eaa7-6800-e651-8bea" value="10.0"/>
      </costs>
    </selectionEntry>
    <selectionEntry id="73d1-55d2-43ea-a386" name="Sword of Battle" publicationId="d9e7-add3-773e-ffab" hidden="false" collective="false" import="true" type="upgrade">
      <constraints>
        <constraint field="selections" scope="roster" value="1.0" percentValue="false" shared="true" includeChildSelections="true" includeChildForces="false" id="ba52-7dc8-2711-86ba" type="max"/>
        <constraint field="selections" scope="parent" value="1.0" percentValue="false" shared="true" includeChildSelections="true" includeChildForces="false" id="e2c5-fb88-6154-79a6" type="max"/>
      </constraints>
      <rules>
        <rule id="df37-0990-29ef-536f" name="Sword of Battle" hidden="false">
          <description>+1 Attack. A Sword of Battle is forged with potent magic that enables its wielder to employ it with dazzling speed and deadly effect. The blade confers +1 Attack on the character wielding it.</description>
        </rule>
      </rules>
      <categoryLinks>
        <categoryLink id="a1f0-39d3-ffb1-ed61" name="New CategoryLink" hidden="false" targetId="e6e5-cff5-9987-d563" primary="true"/>
      </categoryLinks>
      <costs>
        <cost name="pts" typeId="eaa7-6800-e651-8bea" value="25.0"/>
      </costs>
    </selectionEntry>
    <selectionEntry id="3c1d-e820-ab6f-4ea1" name="Sword of Might" publicationId="d9e7-add3-773e-ffab" hidden="false" collective="false" import="true" type="upgrade">
      <constraints>
        <constraint field="selections" scope="roster" value="1.0" percentValue="false" shared="true" includeChildSelections="true" includeChildForces="false" id="a8ff-d3d7-e8ac-d158" type="max"/>
        <constraint field="selections" scope="parent" value="1.0" percentValue="false" shared="true" includeChildSelections="true" includeChildForces="false" id="c150-abce-90f8-9b59" type="max"/>
      </constraints>
      <rules>
        <rule id="5bf0-7276-65a3-5f3d" name="Sword of Might" hidden="false">
          <description>+1 Strength. A Sword of Might is wrought with enchantments that bind within its fabric a great and magical strength. The blade confers +1 Strength upon the character who fights with it.</description>
        </rule>
      </rules>
      <categoryLinks>
        <categoryLink id="6b72-5104-7421-c01f" name="New CategoryLink" hidden="false" targetId="e6e5-cff5-9987-d563" primary="true"/>
      </categoryLinks>
      <costs>
        <cost name="pts" typeId="eaa7-6800-e651-8bea" value="20.0"/>
      </costs>
    </selectionEntry>
    <selectionEntry id="546d-e9a9-3084-27c1" name="Sword of Striking" publicationId="d9e7-add3-773e-ffab" hidden="false" collective="false" import="true" type="upgrade">
      <constraints>
        <constraint field="selections" scope="roster" value="1.0" percentValue="false" shared="true" includeChildSelections="true" includeChildForces="false" id="a09b-a6ce-c3b7-9b00" type="max"/>
        <constraint field="selections" scope="parent" value="1.0" percentValue="false" shared="true" includeChildSelections="true" includeChildForces="false" id="f186-b47a-6d9f-8ea2" type="max"/>
      </constraints>
      <rules>
        <rule id="2ea2-ba4d-9c93-5907" name="Sword of Striking" hidden="false">
          <description>+1 To Hit. A Sword of Striking is possessed of a keen intelligence that guides its blade to the target. The sword confers a dice bonus of +1 to the character wielding it. For example, where 3 is normally required to score a hit, the character will hit on a 2. However, a dice roll of 1 is always a miss regardless of bonuses - the minimum successful roll to hit is therefore 2.</description>
        </rule>
      </rules>
      <categoryLinks>
        <categoryLink id="2391-a436-fa7d-de20" name="New CategoryLink" hidden="false" targetId="e6e5-cff5-9987-d563" primary="true"/>
      </categoryLinks>
      <costs>
        <cost name="pts" typeId="eaa7-6800-e651-8bea" value="30.0"/>
      </costs>
    </selectionEntry>
    <selectionEntry id="0187-c1bd-3c63-16b4" name="Talisman of Protection" publicationId="d9e7-add3-773e-ffab" hidden="false" collective="false" import="true" type="upgrade">
      <constraints>
        <constraint field="selections" scope="roster" value="1.0" percentValue="false" shared="true" includeChildSelections="true" includeChildForces="false" id="0762-c79c-eb8b-1837" type="max"/>
        <constraint field="selections" scope="parent" value="1.0" percentValue="false" shared="true" includeChildSelections="true" includeChildForces="false" id="9734-739d-b49a-9901" type="max"/>
      </constraints>
      <rules>
        <rule id="bf5f-24f9-ce07-a325" name="Talisman of Protection" hidden="false">
          <description>6+ Ward Save. The Talisman of Protection is a protective charm. This confers upon its wearer a Ward save of 6+.</description>
        </rule>
      </rules>
      <categoryLinks>
        <categoryLink id="5fdf-1e08-955d-f262" name="New CategoryLink" hidden="false" targetId="d777-f2f1-e0db-8e8e" primary="true"/>
      </categoryLinks>
      <costs>
        <cost name="pts" typeId="eaa7-6800-e651-8bea" value="15.0"/>
      </costs>
    </selectionEntry>
    <selectionEntry id="eca1-46d6-8778-847f" name="Battle Standard Bearer" publicationId="d9e7-add3-773e-ffab" hidden="false" collective="false" import="true" type="upgrade">
      <modifiers>
        <modifier type="set" field="hidden" value="true">
          <conditions>
            <condition field="selections" scope="parent" value="1.0" percentValue="false" shared="true" includeChildSelections="false" includeChildForces="false" childId="cf7b-798c-9b94-df74" type="equalTo"/>
          </conditions>
        </modifier>
        <modifier type="set" field="f08c-8a0b-9256-2f99" value="1.0">
          <conditions>
            <condition field="selections" scope="primary-catalogue" value="0.0" percentValue="false" shared="true" includeChildSelections="false" includeChildForces="false" childId="05b9-5022-67cd-4fd3" type="instanceOf"/>
          </conditions>
        </modifier>
      </modifiers>
      <constraints>
        <constraint field="selections" scope="roster" value="1.0" percentValue="false" shared="true" includeChildSelections="true" includeChildForces="true" id="6dd5-067c-7aff-21f2" type="max"/>
        <constraint field="selections" scope="parent" value="1.0" percentValue="false" shared="true" includeChildSelections="true" includeChildForces="true" id="3c37-54f3-956f-05ce" type="max"/>
        <constraint field="selections" scope="roster" value="0.0" percentValue="false" shared="true" includeChildSelections="true" includeChildForces="true" id="f08c-8a0b-9256-2f99" type="min"/>
      </constraints>
      <costs>
        <cost name="pts" typeId="eaa7-6800-e651-8bea" value="25.0"/>
      </costs>
    </selectionEntry>
    <selectionEntry id="cf7b-798c-9b94-df74" name="General" hidden="false" collective="false" import="true" type="upgrade">
      <constraints>
        <constraint field="selections" scope="roster" value="1.0" percentValue="false" shared="true" includeChildSelections="true" includeChildForces="true" id="7089-0e82-70a8-4619" type="max"/>
        <constraint field="selections" scope="roster" value="1.0" percentValue="false" shared="true" includeChildSelections="true" includeChildForces="true" id="5874-5ad5-4ab0-9f4d" type="min"/>
        <constraint field="selections" scope="parent" value="1.0" percentValue="false" shared="true" includeChildSelections="true" includeChildForces="true" id="9b1f-4349-b167-f0fa" type="max"/>
      </constraints>
      <categoryLinks>
        <categoryLink id="c021-4783-1580-5475" name="General" hidden="false" targetId="1a61-9b9e-0b56-e6ce" primary="false"/>
      </categoryLinks>
      <costs>
        <cost name="pts" typeId="eaa7-6800-e651-8bea" value="0.0"/>
      </costs>
    </selectionEntry>
    <selectionEntry id="aa12-5ee9-b575-c4a6" name="Lore of Fire" hidden="false" collective="false" import="true" type="upgrade">
      <rules>
        <rule id="7024-2978-a5b8-7165" name="Lore of Fire" hidden="false">
          <description>All of these spells are considered to be Fire attacks and cause double damage against flammable creatures.

The Lore of Fire Lore</description>
        </rule>
      </rules>
      <costs>
        <cost name="pts" typeId="eaa7-6800-e651-8bea" value="0.0"/>
      </costs>
    </selectionEntry>
    <selectionEntry id="2030-7bd3-3f77-1594" name="Lore of Metal" hidden="false" collective="false" import="true" type="upgrade">
      <rules>
        <rule id="c6c8-6225-afec-6763" name="Lore of Metal" hidden="false">
          <description>In the lands of Men, the Lore of Metal is more commonly known as Alchemy. It is practiced by many races, but few are as devoted to it as Men. If there is truth in common talk then there are many fortunes won by means of alchemical sorcery. The Alchemists of the Golden Order at Altdorf have the Emperor&apos;s ear in all matters of state and war – or so it is said by ordinary folk of the town.

The Lore of Metal Lore</description>
        </rule>
      </rules>
      <costs>
        <cost name="pts" typeId="eaa7-6800-e651-8bea" value="0.0"/>
      </costs>
    </selectionEntry>
    <selectionEntry id="8704-072d-b3dd-84f5" name="Lore of Shadow" hidden="false" collective="false" import="true" type="upgrade">
      <rules>
        <rule id="81ba-bf60-d544-9cd7" name="Lore of Shadow" hidden="false">
          <description>In the land of the Empire, Wizards of the Shadow call themselves Grey Wizards, as if to distance themselves from the sinister reputation of their sorcery. They are more often called Trickster Wizards by the common folk, who mistrust and fear them. Shadow Lore is the magic of deceit and illusion, of trickery, concealment and darkness.

The Lore of Shadow Lore</description>
        </rule>
      </rules>
      <costs>
        <cost name="pts" typeId="eaa7-6800-e651-8bea" value="0.0"/>
      </costs>
    </selectionEntry>
    <selectionEntry id="e33d-6dcc-3793-da4a" name="Lore of Light" hidden="false" collective="false" import="true" type="upgrade">
      <rules>
        <rule id="11c9-1d6b-6097-f595" name="Lore of Light" hidden="false">
          <description>The Lore of Light is a magic of bright and radiant power, of the solar wind, and of life giving energy. Wizards who practice this art are sometimes called White Wizards or Hierophants. It is the magic of solar rituals, carefully guarded secrets and ancient ceremonies.

The Lore of Light Lore</description>
        </rule>
      </rules>
      <costs>
        <cost name="pts" typeId="eaa7-6800-e651-8bea" value="0.0"/>
      </costs>
    </selectionEntry>
    <selectionEntry id="7e93-afdd-d365-6a23" name="Lore of Life" hidden="false" collective="false" import="true" type="upgrade">
      <rules>
        <rule id="b257-f163-9a6e-9016" name="Lore of Life" hidden="false">
          <description>The Lore of Life is the magical lore of the growing earth and as such is bound to the changing seasons. Few creatures of any race understand the nature of growing things as do these Wizards. It is a form of magic that exists in all water and vegetation and which is strongest when it is close to places where rivers run and where woods and forests grow most abundantly.

The Lore of Life Lore</description>
        </rule>
      </rules>
      <costs>
        <cost name="pts" typeId="eaa7-6800-e651-8bea" value="0.0"/>
      </costs>
    </selectionEntry>
    <selectionEntry id="adb8-37e0-7609-365b" name="Lore of Death" hidden="false" collective="false" import="true" type="upgrade">
      <rules>
        <rule id="0458-d407-7832-a535" name="Lore of Death" hidden="false">
          <description>Though the Lore of Death, or Amethyst magic, is the most feared of sorceries, not all practitioners are evil or ill-intended. It is the magic of the bygone ages and draws its power deeply from the realm of the dead.

The Lore of Death Lore</description>
        </rule>
      </rules>
      <costs>
        <cost name="pts" typeId="eaa7-6800-e651-8bea" value="0.0"/>
      </costs>
    </selectionEntry>
    <selectionEntry id="afbd-2b69-4e54-2863" name="Lore of Beasts" hidden="false" collective="false" import="true" type="upgrade">
      <rules>
        <rule id="7160-91b1-3786-8d86" name="Lore of Beasts" hidden="false">
          <description>The Lore of Beasts is the magic of Shamans and animal spirits. It is a sorcery of wild and primitive races, of creatures that shun the cities of Men, and of Men who have turned their backs upon the ways of their own kind.

The Lore of Beasts Lore</description>
        </rule>
      </rules>
      <costs>
        <cost name="pts" typeId="eaa7-6800-e651-8bea" value="0.0"/>
      </costs>
    </selectionEntry>
    <selectionEntry id="22d4-14a2-c884-9120" name="Lore of Heavens" hidden="false" collective="false" import="true" type="upgrade">
      <costs>
        <cost name="pts" typeId="eaa7-6800-e651-8bea" value="0.0"/>
      </costs>
    </selectionEntry>
    <selectionEntry id="2be9-2fdd-98db-e42c" name="Power Stone" hidden="false" collective="false" import="true" type="upgrade">
      <rules>
        <rule id="130f-0831-64a4-4e02" name="Power Stone" hidden="false">
          <description>The Power Stone is imbued with a powerful magical invocation. When it is held out by a Wizard before he casts a spell, the effect is to enhance the efficacy of the magic. A further two dice are added to the Casting roll. Note that using a Power Stone will allow a Wizard to use more Power dice than he is normally permitted. For example, a First Level Wizard may read a Power Stone and thus use four Power dice to cast a spell (2 basic + 2 from a Power Stone). A Power Stone can only be used once - after one use its power is exhausted.

Using a Power Stone will bring any spell in play cast earlier by that Wizard to an end in the same way as casting a new spell by ordinary means.

As with scrolls, Power Stones are not unique items - they are prepared by a Wizard prior to battle and it is quite possible for several Wizards to carry Power Stones, and for a Wizard to carry more than one. However, only one Power Stone can be used to enhance a spell.

Note that a spell cast with a Power Stone can never be cast with Irresistible Force, though it can be Miscast.</description>
        </rule>
      </rules>
      <categoryLinks>
        <categoryLink id="7af5-93e3-7411-71f3" name="Arcane Item" hidden="false" targetId="7cfd-b676-48e1-6eec" primary="false"/>
      </categoryLinks>
      <costs>
        <cost name="pts" typeId="eaa7-6800-e651-8bea" value="25.0"/>
      </costs>
    </selectionEntry>
    <selectionEntry id="4707-962c-df84-6b66" name="Power Stones" hidden="false" collective="false" import="true" type="upgrade">
      <constraints>
        <constraint field="selections" scope="roster" value="1.0" percentValue="false" shared="true" includeChildSelections="true" includeChildForces="true" id="a97b-f979-f41e-0a06" type="max"/>
      </constraints>
      <entryLinks>
        <entryLink id="3497-d817-cd35-fc12" name="Power Stone" hidden="false" collective="false" import="true" targetId="2be9-2fdd-98db-e42c" type="selectionEntry">
          <constraints>
            <constraint field="selections" scope="parent" value="1.0" percentValue="false" shared="true" includeChildSelections="false" includeChildForces="false" id="4d47-6a9c-133b-4a47" type="min"/>
          </constraints>
          <rules>
            <rule id="8b10-0186-fa23-f4cc" name="Power Stones" hidden="false">
              <description>The Power Stone is imbued with a powerful magical invocation. When it is held out by a Wizard before he casts a spell, the effect is to enhance the efficacy of the magic. A further two dice are added to the Casting roll. Note that using a Power Stone will allow a Wizard to use more Power dice than he is normally permitted. For example, a First Level Wizard may read a Power Stone and thus use four Power dice to cast a spell (2 basic + 2 from a Power Stone). A Power Stone can only be used once - after one use its power is exhausted.

Using a Power Stone will bring any spell in play cast earlier by that Wizard to an end in the same way as casting a new spell by ordinary means.

As with scrolls, Power Stones are not unique items - they are prepared by a Wizard prior to battle and it is quite possible for several Wizards to carry Power Stones, and for a Wizard to carry more than one. However, only one Power Stone can be used to enhance a spell.

Note that a spell cast with a Power Stone can never be cast with Irresistible Force, though it can be Miscast.</description>
            </rule>
          </rules>
        </entryLink>
      </entryLinks>
      <costs>
        <cost name="pts" typeId="eaa7-6800-e651-8bea" value="0.0"/>
      </costs>
    </selectionEntry>
  </sharedSelectionEntries>
  <sharedSelectionEntryGroups>
    <selectionEntryGroup id="3c79-613e-77df-160c" name="Lore of Magic" hidden="false" collective="false" import="true">
      <constraints>
        <constraint field="selections" scope="parent" value="1.0" percentValue="false" shared="true" includeChildSelections="false" includeChildForces="false" id="03b2-ccac-049b-0200" type="min"/>
        <constraint field="selections" scope="parent" value="1.0" percentValue="false" shared="true" includeChildSelections="false" includeChildForces="false" id="6e37-83cf-ea34-29f2" type="max"/>
      </constraints>
      <entryLinks>
        <entryLink id="c650-1366-8178-c472" name="Lore of Fire" hidden="false" collective="false" import="true" targetId="aa12-5ee9-b575-c4a6" type="selectionEntry"/>
        <entryLink id="25f4-ce32-1f22-e740" name="Lore of Heavens" hidden="false" collective="false" import="true" targetId="22d4-14a2-c884-9120" type="selectionEntry"/>
        <entryLink id="809a-408b-59ab-c2ef" name="Lore of Beasts" hidden="false" collective="false" import="true" targetId="afbd-2b69-4e54-2863" type="selectionEntry"/>
        <entryLink id="7410-aa91-98e2-ab1d" name="Lore of Death" hidden="false" collective="false" import="true" targetId="adb8-37e0-7609-365b" type="selectionEntry"/>
        <entryLink id="4187-99c0-7551-374f" name="Lore of Life" hidden="false" collective="false" import="true" targetId="7e93-afdd-d365-6a23" type="selectionEntry"/>
        <entryLink id="8407-fa2f-cd31-3ddf" name="Lore of Metal" hidden="false" collective="false" import="true" targetId="2030-7bd3-3f77-1594" type="selectionEntry"/>
        <entryLink id="48b7-af3c-59f4-cde2" name="Lore of Shadows" hidden="false" collective="false" import="true" targetId="8704-072d-b3dd-84f5" type="selectionEntry"/>
        <entryLink id="422f-2e3a-6860-98b2" name="Lore of Light" hidden="false" collective="false" import="true" targetId="e33d-6dcc-3793-da4a" type="selectionEntry"/>
      </entryLinks>
    </selectionEntryGroup>
    <selectionEntryGroup id="ed43-1e9a-5409-abc6" name="Wizard Level (Hero)" hidden="false" collective="false" import="true" defaultSelectionEntryId="ade6-41fa-be3c-63f3">
      <modifiers>
        <modifier type="set" field="name" value="Wizard Level"/>
      </modifiers>
      <constraints>
        <constraint field="selections" scope="parent" value="1.0" percentValue="false" shared="true" includeChildSelections="false" includeChildForces="false" id="beb4-282a-e68f-2a41" type="max"/>
        <constraint field="selections" scope="parent" value="1.0" percentValue="false" shared="true" includeChildSelections="false" includeChildForces="false" id="65d6-eea6-c7ff-79ad" type="min"/>
      </constraints>
      <selectionEntries>
        <selectionEntry id="ade6-41fa-be3c-63f3" name="Level 1" hidden="false" collective="false" import="true" type="upgrade">
          <costs>
            <cost name="pts" typeId="eaa7-6800-e651-8bea" value="0.0"/>
          </costs>
        </selectionEntry>
        <selectionEntry id="19e9-4c56-fe42-fbff" name="Level 2" hidden="false" collective="false" import="true" type="upgrade">
          <costs>
            <cost name="pts" typeId="eaa7-6800-e651-8bea" value="35.0"/>
          </costs>
        </selectionEntry>
      </selectionEntries>
    </selectionEntryGroup>
    <selectionEntryGroup id="afae-7702-64a2-3f42" name="Wizard Level (Lord)" hidden="false" collective="false" import="true" defaultSelectionEntryId="9000-07c6-76b9-495c">
      <modifiers>
        <modifier type="set" field="name" value="Wizard Level"/>
      </modifiers>
      <constraints>
        <constraint field="selections" scope="parent" value="1.0" percentValue="false" shared="true" includeChildSelections="false" includeChildForces="false" id="2b51-14fa-5a5e-9edd" type="max"/>
        <constraint field="selections" scope="parent" value="1.0" percentValue="false" shared="true" includeChildSelections="false" includeChildForces="false" id="4614-7ac7-c5e4-487f" type="min"/>
      </constraints>
      <selectionEntries>
        <selectionEntry id="9000-07c6-76b9-495c" name="Level 3" hidden="false" collective="false" import="true" type="upgrade">
          <costs>
            <cost name="pts" typeId="eaa7-6800-e651-8bea" value="0.0"/>
          </costs>
        </selectionEntry>
        <selectionEntry id="2143-da8f-19dd-194f" name="Level 4" hidden="false" collective="false" import="true" type="upgrade">
          <costs>
            <cost name="pts" typeId="eaa7-6800-e651-8bea" value="35.0"/>
          </costs>
        </selectionEntry>
      </selectionEntries>
    </selectionEntryGroup>
    <selectionEntryGroup id="469b-afc2-4a50-5910" name="Power Stones" hidden="false" collective="false" import="true">
      <constraints>
        <constraint field="selections" scope="roster" value="1.0" percentValue="false" shared="true" includeChildSelections="true" includeChildForces="true" id="ddb3-6c10-db11-1780" type="max"/>
      </constraints>
      <entryLinks>
        <entryLink id="78a6-2490-21c8-f77b" name="Power Stone" hidden="false" collective="false" import="true" targetId="2be9-2fdd-98db-e42c" type="selectionEntry"/>
      </entryLinks>
    </selectionEntryGroup>
  </sharedSelectionEntryGroups>
  <sharedRules>
    <rule id="ec06-621f-83ae-fd4c" name="Scouts" hidden="false">
      <description>Scouts are set up after both armies have been deployed. They can be set up anywhere on the table, at least 10&quot; away from the enemy and must be out of the sight of any enemy troops and in or behind interposing terrain (not out in the open!). If both armies contain troops with this ability, each player should roll a D6, with the player scoring the highest choosing whether be deploys before or after the enemy&apos;s Scouts. Two opposing groups of Scouts cannot be set up within 10&quot; of each other.

Alternatively, Scouts can be placed on the controlling player&apos;s deployment zone like any other troops, after deployment of both main armies is finished.</description>
    </rule>
    <rule id="4c3d-1a6a-3977-0b53" name="Skirmishers" hidden="false">
      <description>Formation. Skirmishers move as a loose group rather than in ranks and files, with models up to 1&quot; apart. If casualties split the group, the player must reform it in his next Movement phase.

Movement. Skirmishers move up to double their Movement characteristic at all times, even within 8&quot; of the enemy. This doubled rate is not doubled again to charge or march. Their standard Movement is still used for flee and pursuit distances.

Manoeuvring. Skirmishing models move like individual characters. The unit never turns or wheels; each model moves in any direction without penalty, and must end within 1&quot; of the group.

Terrain. Skirmishers suffer no movement penalty for crossing obstacles or moving through difficult or very difficult ground.

Shooting. Skirmishers may shoot in any direction. They do not block the line of sight of their own unit, including a character who has joined them, but a skirmishing unit does block line of sight to other units. An enemy shooting at skirmishers suffers -1 to hit; this applies only once, even if a character is with the unit. A skirmisher that moved faster than its standard Movement may not shoot that turn.

Close combat. Skirmishers may charge any enemy visible to at least one model, and form up into a fighting line. In combat they never receive a rank bonus, and do not negate an enemy&apos;s rank bonus by charging its flank or rear. Once formed up they do have flanks and a rear, which count for combat resolution bonuses if the skirmisher unit is subsequently charged by another enemy unit. They overrun straight ahead, as other units do.

Characters. Only a roughly man-sized character on foot may join a skirmishing unit.</description>
    </rule>
    <rule id="d168-689e-84dd-9b7e" name="Poisoned Attacks" hidden="false">
      <description>A warrior with poisoned attacks will wound his target automatically if he scores a 6 when determining whether he hits his opponent in the Shooting or Close Combat phases. Armour saves are taken as normal. Unliving targets (such as war machines) are immune to poison as are some troop types. These are clearly defined in their description.</description>
    </rule>
    <rule id="87db-2d4c-3fa6-6a26" name="Fly" hidden="false">
      <description>In Warhammer, flight is represented by a &apos;long swoop&apos; or &apos;glide&apos; of up to 20&quot;. The flyer starts off on the ground, takes off, flies to where it wishes to go, and then lands. Flyers, therefore, begin and end their movement on the ground. Flyers never need to wheel or turn, but can always make their move in a direct line. Of course, they still need to see any target they want to charge or shoot at and have a 90° arc of sight to their front, as normal.

Flyers do not benefit from the extra Move distance conferred on ground moving models for charging or marching. The flying move is never doubled and flyers charge at normal speed as explained later.

A flyer may charge an enemy within its 20&quot; flight move. The charge must be declared in the normal way and the enemy has the usual response options. The flying move is not doubled Like a ground charge is. Note that a flyer must be able to see its intended target when charges are declared as normal, and can fly over models and scenery which would stop the charge of a normal model. Flyers that charge their enemy are placed into base contact with the enemy unit in a normal manner (ie, flyers are positioned to the sides if the attack comes from the flank, to the rear if it comes from behind, etc).

Flyers suffer no movement penalties for changing direction, overflying scenery, or crossing obstacles. They may overfly other models, including enemy troops, without penalty. Flyers may not move, land in or take off from within a wood. If flyers wish to enter a wood, they must land outside it and walk inside using their ground movement in the next turn. Note that this applies to any terrain that both players consider would prohibit flying.
Flyers may not land on top of enemy formations - if they wish to attack an enemy they must engage in combat as described above.

The distance flyers flee is usually based on their flying Move rather than their ground Move. The normal flee distance for flyers is therefore 3D6&quot; in common with all models whose move is more than 6&quot;. If flyers must flee along the ground due to some constraint which prevents them from flying, for example, if they are in me middle of a wood, then they flee 2D6&quot; or 3D6&quot; depending on their Movement characteristic, just like other troops.

Flyers pursue fleeing enemy in exactly the same way as ordinary troops. Their normal pursuit rate is therefore 3D6&quot; and the same comments apply as for fleeing.

Most flyers are monsters, but some units of troops can fly too. Such units are clearly identified in their army lists. They follow all the normal rules for flyers given above, apart from the exceptions noted below.
- Flying units always operate as skirmishers.
- Characters can never join units of flyers, even if they ride flying creatures. This is because characters ride large flying monsters, which are nowhere near as manoeuvrable as me light, fast creatures of flying units and will slow them down considerably.</description>
    </rule>
    <rule id="03be-3e56-1332-bf56" name="Fear" hidden="false">
      <description>Fear is a natural reaction to huge or especially ugly and unnerving monsters. Some creatures inspire fear as is indicated in their relevant Army book and these include large and disturbing monsters such as Troll; as well as supernatural horrors such as Skeletons.

A unit must take a Fear test if it is faced by one of the following situations:

1. If Charged by a Fear-causing Enemy
2. If a Unit Wishes to Charge a Feared Enemy</description>
    </rule>
    <rule id="3767-0d81-4db9-cda7" name="Terror" hidden="false">
      <description>Some monsters are so huge and threatening that they are considered to be even more frightening than those described by the Fear rules. Such creatures cause terror.

Troops who are confronted by monsters or situations that cause terror must test to see whether they overcome their terror. If they fail, they are completely terrified and are reduced to gibbering wrecks. Troops only ever test for terror once in a battle. Once they&apos;ve overcome their terror they are not affected again.

If a creature causes terror then it automatically causes fear as well, and all the rules described for fear apply. However, you never have to take a Terror and a Fear test from the same enemy or situation - just take a Terror test: if you pass the Terror test then you automatically pass the Fear test, too. As any unit of Troops only ever takes one Terror test in a battle, any subsequent encounters with terrifying monsters or situations will simply count as fear.

- A unit must make a Terror test if charged by or wishing to charge an enemy that causes terror.
- A unit must make a Terror test at the start of its turn if there is an enemy which causes terror within 6&quot;.</description>
    </rule>
    <rule id="6c1b-2f0f-d172-01ca" name="Stupidity" hidden="false">
      <description>Many large and powerful creatures are unfortunately rather stupid. Even some otherwise quite intelligent creatures act stupidly now and again because they are readily confused or distracted, or perhaps because they are drugged or have been knocked insensible. The Stupidity rules represent the sort of slow wittedness or dumb behaviour which some especially stolid or stubborn beasts are prone to. Creatures that, are stupid are indicated in the Army books and include such monstrous creatures as Trolls.

Stupid creatures must make a test at the start of their turn to see whether they overcome their stupidity. Make a test for each unit of stupid troops. If they pass the test by rolling their Leadership value or less on 2D6 then all is well and good - the creatures behave reasonably intelligently and can move and fight as normal. Nothing untoward has occurred beyond a bit of drooling and the odd spontaneous cackle.

If the test is failed then all is not well. The following rules apply until the creatures&apos; following turn when they must test once more to see whether they are overcome by stupidity. In addition, a Wizard subject to being stupid cannot cast spells if he fails the test.

1. If already in close combat, half of the stupid creatures in base contact with the enemy suddenly stop fighting. They stare around blankly and wonder where they are. If the unit has an odd number of models or if a stupid creature is fighting on its own then roll a D6. If the result is 4 or more, the odd model fights; if not, it stands around vacantly. Note that only stupid creatures are affected. If a unit contains stupid creatures and other creatures (a unit of Trolls led by a Goblin Chieftain, for example) then the other creatures are not affected. The controlling player decides which individual creatures in combat cannot fight.
2. If not in close combat, the unit momentarily forgets what it is doing. Move the unit directly forwards at half normal speed (for example, Trolls with Movement 6 would move 3&quot; forward). Any enemy troops encountered are automatically charged. If there are friends in the way, both units blunder into each other and their ranks become confused, in which case both units are pinned in place for the rest of the turn and neither may move further. This counts as compulsory movement and so occurs before other movement, but after charges have been declared (see the Movement section). Creatures within the unit that do not suffer from being stupid must also move as described - they are carried along by the movement of the rest of the unit and risk being trampled if they attempt to do otherwise.</description>
    </rule>
    <rule id="01c3-c8c6-431f-1c2b" name="Large Target" hidden="false">
      <description>&gt; Note: This is a custom special rule that does not appear as a specified rule in the Main Rulebook. References to large targets appear frequently and this compiles the rules from To Hit Modifiers and Who Can Shoot and Line of Sight into a single instance that covers the features of large targets.

A large target is anything which in real life would be massively tall or which is especially bulky. Giants are large targets, for example, while Men, Orcs, Elves, Ogres, Cannons and the vast majority of troops are not. In every case, a creature&apos;s description in the relevant Army book will inform you whether it is a large target or not. Cavalry riders are not considered to be large targets if they are riding horses, wolves, boars or comparable beasts. Dragons, Greater Daemons and certain war machines are large targets. The following rules apply to large targets:

- Units which are shooting at a large target get a +1 to hit bonus.
- Large targets can see and shoot at targets over interposing models normal-sized models (and vice versa).
- Large targets moving along the ground cannot charge through any interposing models.</description>
    </rule>
    <rule id="f6c9-ac44-1d7c-ed6e" name="Unbreakable" hidden="false">
      <description>These troops never break in close combat, and they are also immune to panic, terror and fear or any other Psychology rules. If defeated in close combat (even by fear-causing creatures that outnumber them) unbreakable troops continue to fight on regardless of results. They may never, however, declare that they are fleeing as a charge reaction, as they will literally die fighting under any circumstances.</description>
    </rule>
    <rule id="512a-5ae5-c6cb-b82a" name="Immune to Psychology" hidden="false">
      <description>Some warriors and creatures in the Warhammer world are almost completely fearless, or such grizzled veterans that scenes which would make lesser troops panic have no effect on them.

Troops that are immune to psychology are never affected by fear, terror, frenzy or any other Psychology rules. Troops immune to Psychology may never flee as a charge reaction - they are far too proud and brave to do this! These troops still have to take Break tests as normal.</description>
    </rule>
    <rule id="a317-ad28-0409-0c8b" name="Frenzy" hidden="false">
      <description>Certain warriors can work themselves into a fighting frenzy, a whirlwind of destruction in which all concern for personal safety is ignored in favour of mindless violence. Many of these frenzied warriors are drugged or tranced, and have driven themselves into a psychotic frenzy with chancing, singing, yelling and screaming. These troops are described as frenzied. In the case of mounted troops, frenzy only affects the riders. No Psychology test is required for frenzy, and the following rules apply automatically:

After charges have been declared, measure to see if any enemies are within charge reach of any frenzied troops (ie, within the unit&apos;s charge move and in their normal charge arc). If so, the frenzied unit must charge that enemy. The player has no choice in the matter; the unit will automatically make its charge move. This automatic charge is done after charges have been declared, but you may declare normal charges with your frenzied troops if you wish. If there are several eligible units within the charge reach of the frenzied unit, the controlling player may decide which unit to charge.

Frenzied troops and characters fight with +1 extra Attack during close combat. Models that have 1 Attack on their profile therefore have 2, troops with 2 Attacks have 3, and so on. If models have an extra weapon then they will receive +1 extra Attack for this as normal, so if they have 1 Attack on their profile, they would receive 2 + 1 = 3 Attacks in total.

Frenzied troops and characters must pursue fleeing enemy whether the player wants them to or not. They even pursue if they are defending an obstacle. Unlike other troops, they may not attempt to hold back as they are far too crazed with battle lust. If they wipe their enemy out in the first Close Combat phase, they will always overrun their opponent. Frenzied troops may not elect to flee if they are charged - their bloodlust overcomes their concerns for safety.</description>
    </rule>
    <rule id="1e41-936a-2bae-76cc" name="Stubborn" hidden="false">
      <description>Some troops will fight on in close combat almost regardless of casualties. This can be because they consider themselves to be elite, have taken severe vows to hold their ground in combat or are simply too dumb to flee when defeated by superior troops! Sometimes troops will fight stubbornly against certain enemies because of honour, vows or racial animosity, and fight normally against other enemies. These troops are referred as being stubborn.

The following rules apply:

Stubborn troops take all Break tests on their unmodified Leadership value. They do not reduce this value regardless of any combat results, how many casualties they have suffered or other combat bonuses. This means, for example, that stubborn troops with a Leadership value of 9 will only ever break on the roll of 10 or more when making a Break test. If a stubborn unit contains characters with higher Leadership values than the rank-and-file troops who are not themselves stubborn, the character&apos;s Leadership value can be used to take the test, but it is still subject to the normal modifiers for a Break test. Use either the Leadership value of the character leading the unit or the unit&apos;s own Leadership value, depending on which results in the higher value for passing a Break test.

Characters that are part of a stubborn unit but are not stubborn themselves will not have to take a separate Break test - they benefit and gain from the determination of the troops around them! Stubborn units led by stubborn characters can use the character&apos;s unmodified Leadership value for Break tests. Note that any troops who are not stubborn but are led by a stubborn character may use his Leadership value for Break tests, but the roll is modified as normal.</description>
    </rule>
    <rule id="2db9-4b87-800e-ed58" name="Hatred" hidden="false">
      <description>Hatred is a powerful emotion and instances of hatred and rivalry are commonplace in the Warhammer world. There are grudges borne over centuries, racial animosity bordering on madness, and irreconcilable feuds that have left generations of dead in their wake. Some races hate other races with such bitter conviction that they will fight with astounding fury. Like frenzy, no Psychology test is taken for hatred.

Troops fighting in close combat with a hated foe may re-roll any misses When they attack in the first turn of any combat. This bonus only applies in the first turn of a combat and represents the unit venting its pent up hatred on the foe. After the initial round of blood mad hacking they lose some impetus and subsequently fight as normal for the rest of the combat.

Troops who hate their enemy must always pursue them if they flee. They cannot attempt to avoid pursuit by testing their Leadership as other troops can. They must even pursue if behind a defended obstacle.</description>
    </rule>
    <rule id="ab75-c6ec-0411-c924" name="Fast Cavalry" hidden="false">
      <description>Fast cavalry use regular formations and follow all the normal rules for units, including penalties in difficult terrain, except as follows. They never receive a rank bonus.

Free reform. Unless it charges, a fast cavalry unit may reform as many times as you wish during its Movement phase with no penalty to its Move distance. No model may move further than its maximum Move despite the free reform.

Shooting. Fast cavalry may shoot all round, regardless of the direction the models face. For charging, stand &amp; shoot reactions and the like, the models must face the enemy as normal. They may shoot even when marching or reforming; the usual -1 to hit for moving applies.

Fleeing and rallying. A fast cavalry unit that flees as a charge reaction and then rallies at the beginning of its next turn may reform facing in any direction and is free to move that Movement phase. If the chargers fail to catch it, their charge fails as normal; if the flee move does not carry it beyond the chargers&apos; reach, the unit is destroyed as normal.

Characters. A character may join a fast cavalry unit and move with it, but does not benefit from any of the special shooting rules.</description>
    </rule>
    <rule id="4bb1-dfab-2824-bad1" name="Chariot" hidden="false">
      <description>The model. A chariot, its crew and the creatures pulling it are a single model - in effect a unit of one, moving and fighting like a character or a large monster. It has separate characteristics for the chariot, the crew and the creatures. A chariot&apos;s Unit Strength equals its Wounds characteristic, or its Wounds +1 if a character is riding it. Spells that move individual models cannot move a chariot.

Movement. A chariot moves at the speed of the creatures pulling it. It may never march, but doubles its move to charge. It does not turn or wheel and may face any direction without penalty, though it still needs line of sight to declare a charge.

Terrain. A chariot may not voluntarily cross obstacles or difficult terrain, except a bridge or ford that is safe to cross. If forced into such terrain it suffers D6 Strength 6 hits, resolved against the chariot.

Impact hits. A charging chariot inflicts D6 hits at its own Strength, +1 with scythed wheels. These are resolved before close combat begins; models killed by them do not fight, and the wounds count towards combat resolution.

Attacks. All crew fight, including the driver, against enemies to the front, side or rear, in normal Initiative order. The creatures pulling the chariot may attack only enemies directly in front of them. The chariot has no Weapon Skill of its own - use the highest of its crew. Crew may shoot as normal, at -1 to hit if the chariot moved.

Damage. A chariot has a single pool of Wounds covering the chariot, crew and creatures; when the last is lost, remove the model. Any wound caused by a hit of Strength 7 or more destroys the chariot outright, with no armour save. Shooting is resolved against the chariot as against any unit, at +1 to hit if it is a Large Target.

Characters. A character rides a chariot as he would a large monster. Shots are randomised: on a 6 the character is hit. He uses either his own armour save +2 or the chariot&apos;s, whichever is better. In close combat the attacker chooses whether to strike the chariot or the character. A character in a chariot may issue or accept a challenge, fighting as though on foot - impact hits and crew and creature attacks are worked against the enemy unit rather than the challenge, unless the enemy character was alone when the chariot charged.

Flee and pursuit. Chariots flee and pursue as ordinary troops, at 2D6&quot; or 3D6&quot; by speed, and are destroyed if caught.

Upgrades. Extra crewman: +1 crew attack. Extra steed: +1 steed attack. Scythed wheels: +1 impact hit.</description>
    </rule>
    <rule id="7c7c-8683-ae17-d576" name="Regeneration" hidden="false">
      <description>A creature with this ability may try to regenerate any wound on a D6 roll of 4+. Only one attempt may be made on each wound to regenerate it.

Troops that are able to can regenerate damage if not too badly hurt. Work this out as follows. When attacked in close combat, shot at, or the target of spells, calculate the number of wounds suffered as normal. Once all attacks for the phase have been made, the creature may try to regenerate. Roll a D6 for each wound suffered during that phase. If a 4 or more is rolled, that wound has regenerated. You may only try to regenerate any single wound once. Any regenerated wounds are reinstated, and models removed as casualties are replaced if enough wounds are regenerated.

The results of combat, panic, etc are worked out after creatures have regenerated (the number of wounds inflicted does not include any that are regenerated).

For example, three Trolls (which can regenerate) are fighting five Empire Knights. The Knights strike first and inflict 5 wounds, enough to kill one Troll and cause 2 further wounds. The remaining two Trolls inflict 3 wounds on the Knights. The Trolls now test to regenerate and successfully regenerate 3 wounds. The 3 wounds are reinstated, the &apos;killed&apos; Troll is replaced, and the 2 wounds suffered are noted down. The Knights have scored only 2 wounds in the end while the Trolls have inflicted 3. Assuming no other combat bonuses apply, the Trolls have won.

Fire

The flesh of a regenerating creature cannot regenerate if it has been burnt. If a regenerating creature or unit sustains one or more wounds from a flame attack it cannot regenerate any wounds during the remainder of the battle, not even those inflicted by ordinary weapons.

Note**: In Warhammer Chronicles 2004, page 114 it was clarified Regeneration has no effect on successful Killing Blows.</description>
    </rule>
    <rule id="773c-6c86-ae53-1cee" name="Killing Blow" hidden="false">
      <description>If a model with the Killing Blow special ability rolls a 6 when rolling to wound, he automatically slays his opponent without recourse to a saving throw, apart from Ward saves.

This attack is only effective against roughly man-sized opponents such as Men, Orcs, Elves, Beastmen, etc. It has no effect on big creatures such as Ogres or Dragons, or things like swarms which consist of several creatures. It can be used against models mounted on steeds or monsters as long as the riders themselves are roughly man-sized.

Note**: From Warhammer Annual 2002, Gav Thorpe clarified Regeneration has no effect on successful Killing Blows.</description>
    </rule>
    <rule id="6e0c-4c98-a2c2-af0d" name="Magic Resistance" hidden="false">
      <description>A creature with magic resistance will be difficult to harm with magic. The number in the brackets indicates the maximum number of extra dice that may be rolled when trying to dispel each spell that affects the magically resistant creature. For details of dispelling see the Magic section.</description>
    </rule>
    <rule id="1a01-bd8c-93eb-8de9" name="Flammable" hidden="false">
      <description>Some creatures, such as Undead Mummies and Treemen, burn easily. A flammable creature hit by a flaming weapon or fiery spell will take double wounds, so every wound suffered by a flammable creature will be doubled to 2 wounds. Take any saves before multiplying the wounds.</description>
    </rule>
    <rule id="ea74-4e81-f844-d146" name="Stone Thrower" publicationId="d9e7-add3-773e-ffab" page="120" hidden="false">
      <description>Work out the results of stone throwing in the Shooting phase. To work out damage you will need the small 3&quot; round template. The stone is not as big as the template of course (that would require a very large engine indeed) but it shatter on impact sending shards of sharp stone over a wide area.

Pivot the stone thrower on the spot so that it is pointing in the direction it is going to shoot. The crew do not need to be able to see their target, but they must see that there are enemy in the direction they are firing. Then declare how far the rock is to be fired. Do this without measuring the distance to that target, so try to guess the range as accurately as possible. Once you have made your guess, place the template directly over that spot where you have guessed.

To decide whether the missile lands where it was aimed roll the Scatter dice and the Artillery dice.

The Scatter dice is the dice marked with arrows on four sides and the HIT symbol on two sides. If a HIT is rolled then the missile lands exactly where it was aimed. If an arrow is rolled then the missile veers off in the direction shown by the arrow.

The Artillery dice is marked 2, 4, 6, 8, 10 and MISFIRE. If a Misfire has been rolled then something has gone wrong - roll a D6 and consult the Stone Thrower Misfire chart. A Misfire roll automatically cancels out the whole shot regardless of the Scatter dice result. If a number on the Artillery dice is rolled then this is the distance in inches the missile veers off target as shown by the arrow on the Scatter dice. Move the template the distance indicated in the direction shown by the arrow. If a HIT has been rolled then the numbers are ignored; a number simply indicates that the shot has not misfired.

Damage:
Once it is established where the stone lands damage can be worked out. Any model that lies completely under the template is hit automatically - models whose bases lie partially under the template are hit on a 4+. You will have to use your judgement and common sense to decide exactly which models lie under the template - sometimes it is not easy to judge precisely.

Once it has been worked out which models are struck, work out damage in the usual way. Roll for each target to see whether it has suffered damage. Stone throwers have a Strength of 4 or more, so they cause damage on the roll of a 3+ or 4+ against most human or similarly sized targets. A damaging hit from a stone thrower causes D6 wounds, but as most creatures have only 1 Wound it is not necessary to take this dice roll. It is, however, useful when attacking characters and big monsters.

Any single model which lies directly at the centre of the template suffers 1 automatic hit at twice the stone thrower&apos;s usual Strength - the stone lands directly on top of that model. This means that a stone thrower can potentially slay even a large monster or a powerful character.

No armour saving throw is permitted against wounds from a stone thrower. Ward saves may be taken as normal.

Loss of Crew:
A stone thrower requires a full crew to work it properly – to carry stones, push then machine round to bear on its target, and so on. If one crewman is slain then the rest can just about get by without slowing up the machine noticeably. If two or more crewmen are slain then the remaining crew will be unable to cope and the stone thrower will have to miss a whole turn before it can shoot again. This is in addition to any penalty imposed by a Misfire result. Obviously, the engine requires at least one crewman to work, so the machine will become useless should they all be slain.</description>
    </rule>
    <rule id="d4c8-556b-9d58-4ca8" name="Stone Thrower Misfire Chart" publicationId="d9e7-add3-773e-ffab" page="120" hidden="false">
      <description>D6		Result
1	Destroyed!	The engine cannot stand the strain placed upon it and breaks under the tension as it is fired. Bits of wood and metal fly all around, the stone tumbles to the ground splintering the engine and throwing debris into the air. The engine is destroyed and its crew slain or injured. Remove the engine and its crew.
2-3	Disabled.	The normal smooth running of the machine and its crew is disrupted by some accident or freak occurrence. A rope snaps and lashes about wildly, a crewman sets the machine up wrongly so that it pulls itself apart, or maybe a careless operator has become entangled in the mechanism. The engine does not shoot this turn and cannot fire next turn either while the damage is repaired. To help you remember, it is a good idea to turn the machine round to face away from the enemy. In addition, one of the crew is slain - caught by a snapping rope, entangled in the machinery, or thrown high into the air in place of the stone!
4-6	May not shoot.	A minor fault prevents the machine shooting this turn. A crewman drops the stone as he lifts it into position, maybe a ratchet jams or a rope loosens. The machine is unharmed and may shoot as normal next turn.</description>
    </rule>
    <rule id="95df-6c33-fb3e-c966" name="Cannon" publicationId="d9e7-add3-773e-ffab" page="122" hidden="false">
      <description>Cannons are fired in the Shooting phase. To fire a cannon, it must first be turned on the spot so it points in the direction of the target which must be within line of sight but otherwise is not limited by targeting restrictions. Then the player must declare how far the cannon is going to shoot - eg, 24&quot;, 30&quot;, 32&quot;, etc.

The cannonball travels the distance that the player has nominated, plus the score from the Artillery dice. Roll this dice and add the score to the distance that has been declared. The cannonball travels the total distance towards the target and will either land short, pass straight over, or hit depending on how accurately the player guessed the range and what effect the dice has.

Remember the dice will always add at least 2&quot; to an estimate, and can add up to 10&quot;, so you should aim a few inches short of the target.

Once it is established where the cannonball hits, place a small coin or other marker directly over the spot. The cannonball does not stop where it hits the ground but bounces straight forward and cuts a line through any targets in the way. To determine how far the cannonball bounces, roll the Artillery dice again and mark the spot where the cannonball comes to land. Any models between the points where the ball strikes the ground and where it eventually comes to land are hit by the flying cannonball. This line is considered to be a template for rules purposes (such as &quot;Look out, Sir!&quot; rolls).

When a cannonball collides through a unit, only one model per rank is hit.

Any model struck by a cannonball takes a Strength 10 hit resolved in the normal manner. If the cannonball wounds its target then it causes not 1 wound but D3 or D6 wounds depending on the size of the cannon - a cannon causes D3 wounds and a great cannon D6. As most models have only 1 Wound anyway it will not be necessary to roll this extra dice, but it is important when it comes to rolling for heroes, big monsters, and engines of war which can take several wounds. Wounds caused by cannon shot cannot be saved by armour. If a cannonball hits a model which has several parts then resolve which part of the model is hit just like shooting with bows, etc.

No armour saving throw is permitted for wounds caused by cannons. If a cannonball hits you, no amount of armour is going to do you any good. Ward saves can be taken as normal.

Instead of firing a normal shot, cannon crew can opt to fire grapeshot instead. Normal targeting rules apply. Grapeshot has a range of 8&quot;. If in range, the target suffers a number of hits equal to the roll of an Artillery dice, resolved at Strength 4, with a -2 Armour save modifier. Misfires occur as normal.

The Artillery dice is rolled twice when a cannon is fired, so there are two chances of rolling a Misfire result. However, the two results will be different. If a Misfire result is rolled on the first dice, the cannon has literally misfired and may explode - roll a D6 and consult the Cannon Misfire chart. If a Misfire is rolled on the Bounce roll then this merely indicates that the ball has stuck in the ground and does not bounce.

Loss of Crew:
A cannon requires a full crew to work properly - to carry cannonballs, load gunpowder, push the machine round to bear on its target, and so on. If one crewman is slain then. the rest can just about get by without reducing the rate of fire. If two or more crewmen are slain than the remaining crew will be unable to cope, so when it shoots the cannon must miss a whole turn before it can shoot again. This is in addition to any penalty imposed by a Misfire result.

Obviously the cannon requires at least one crewman to work it, so the machine becomes useless should they all be slain.</description>
    </rule>
    <rule id="f957-e84a-67fd-28cc" name="Cannon Misfire Chart" publicationId="d9e7-add3-773e-ffab" page="123" hidden="false">
      <description>D6		Result
1	Destroyed!	The cannon explodes with a mighty crack. Shards of metal and wood fly in all directions leaving a hole in the ground and a cloud of black smoke. The cannon is destroyed and its crew slain or injured. Remove the cannon and its crew.
2-3	Malfunction.	The powder fails to ignite and the cannon does not fire. The crew must remove the ball and powder before the cannon can shoot again - which takes another turn. The cannon therefore cannot fire either this turn or the next turn. It is a good idea to turn the cannon round to indicate this.
4-6	May not shoot.	A minor fault prevents the cannon from firing this turn, perhaps the fuse is not set properly or maybe the crewmen mishandle the loading procedure. The cannon is unharmed and may shoot as normal next turn.

If you roll a Misfire on your Bounce roll then the cannon is unharmed, the misfire result merely indicates that the cannon ball has struck in the ground where it hits. If the shot lands on top of a model then that particular model is hit as normal, but there is no further bounce damage.</description>
    </rule>
    <rule id="3702-c42a-047c-af5f" name="Bolt Throwers" publicationId="d9e7-add3-773e-ffab" page="124" hidden="false">
      <description>Bolt throwers are fired in the Shooting phase along with other missile weapons. To fire a bolt thrower it must first be turned on the spot so that it points towards its intended victim. The bolt travels straight forward and (hopefully) hits the first target in its path. In a unit of troops this will always be a regular trooper. Only if there are no rank-and-file troops in the first rank hit by the bolt will it be necessary to randomize which model in the front rank is hit.

To determine whether the bolt strikes its target, roll a D6 to hit using the crew&apos;s BS in the same way as bow shots, crossbows, and other missile weapons. The usual modifiers apply, except no penalty is imposed for turning the machine, as it is designed to be used in this way. See the Shooting section for details.

If a hit is scored work our damage as described below. If the shot misses then the bolt hits the ground or sails into the air and comes down harmlessly somewhere else.

A bolt thrower is a powerful weapon which can hurl its bolt through several ranks of troops, piercing each warrior in turn. If it hits then resolve damage against the target using the bolt thrower&apos;s full Strength of 6. If the model hit in the first rank is slain then the bolt hits the trooper in the second rank directly behind: resolve damage on the second model with a Strength of 5. If the second rank trooper is slain than a model in the third rank is hit: resolve damage with a Strength of 4. Continue to work out damage as the bolt pierces and slays a model in each rank, deducting -1 from the Strength for each rank pierced.

A model damaged by a bolt thrower sustains not 1 but D3 wound, which means that even large monsters can be hurt or slain by a hit front a bolt thrower. Armour saves are not allowed for hits from a bolt thrower because the missiles are so fast and deadly that any armour is pierced along with its wearer. As saves are not taken, a target with only 1 Wound will be slain if it takes damage, there is no need to roll the D3 to decide the number of wounds. Remember that ward saves can be taken as normal against damage from a bolt thrower.

Loss of Crew:
Some bolt throwers have a crew of two and if one crewman is slain then the remaining crewmen can just about get by without slowing up the machine noticeably. Should a bolt thrower require a larger crew, then the loss of a second crewman will reduce its rate of fire to every second turn in the same way as for stone throwers and cannons.</description>
    </rule>
    <rule id="2381-ed16-2a32-cd12" name="Breath Weapon" hidden="false">
      <description>A model with a breath weapon may use it in the Shooting phase. Use the Flame template, placing the broad end over your intended target as you wish and the narrow end next to the creature&apos;s head. Any model that lies completely under the template is hit automatically - models whose bases lie partially under the template are hit on a 4+. The strength and any special effects of the breath weapon will be detailed in the entry for each individual creature. Characters under the template are eligible for &apos;Look out, Sir!&apos; rolls if they are in a unit.

Breath weapons may not be used as a stand &amp; shoot charge reaction, and neither can they be used in close combat. A creature with a breath weapon needs time to belch forth its flames!</description>
    </rule>
    <rule id="3783-e8d5-f94a-7b2c" name="Small" hidden="false">
      <description>Units with this special rule do not block the line of sight of other units. Note that this does not, however, allow other skirmishers to move through their formation.</description>
    </rule>
    <rule id="21d5-5848-02a7-f995" name="Swarm" hidden="false">
      <description>Swarms represent many creatures on a single 40mm × 40mm base. This base is treated as a single model with several Wounds and Attacks. A Swarm base fights at full effect until it has taken all it&apos;s wounds then it is removed. Swarms are Unbreakable and cannot be joined by characters.</description>
    </rule>
    <rule id="7eca-56b9-d1c7-c7c8" name="Scaly Skin" hidden="false">
      <description>Some creatures, the reptilian Lizardmen in particular, have tough, scaly skin which acts exactly like armour. This save can be variable. Lizardmen Skinks, for example, have a scaly skin save of 6+, while mighty Dragons could have a save of 3+ or more! The effectiveness of the scaly skin can be combined with armour, so a model with a 5+ scaly skin save and a shield would have a 4+ save. Note that scaly skin is an armour save for all intents and purposes, and may be modified by high Strength, etc.</description>
    </rule>
    <rule id="afee-6689-856e-2974" name="Wizard Levels" hidden="false">
      <description>Level 2: Wizards of the Second Level are experienced spell casters whose powers are significantly greater than mere First Level Wizards.

Level 3: Wizards of the Third Level are great sorcerers of a kind rarely seen on the battlefield except in times of dire need.

Level 4: Wizards of the Fourth Level are the most mighty of all Wizards, the very equals of kings amongst the realms of sorcery.

The higher a Wizard&apos;s Level, the greater his ability to draw magical power from the swirling winds of magic, either for his own use or that of his fellow Wizards.

Each Wizard begins the game with one pre-generated spell for each Magic Level he has. We&apos;ll explain how to generate spells later. For now it is sufficient to know that First Level Wizards have one spell, Second Level Wizards have two spells, and so on.</description>
    </rule>
    <rule id="f7df-1ae0-6688-5c38" name="Musicians" hidden="false">
      <description>An army marches under its banners but it does so to the beat of drums and the call of blaring horns. A unit of troops may include a Musician model, either a horn blower or a drummer, to accompany it into battle. Like Standard Bearers, Musicians fight just like an ordinary member of their unit, even if the model itself has slight variances in armour or weaponry. Also Like Standard Bearers, the player does not have to remove Musicians but can substitute an ordinary model instead. Unlike Standard Bearers, Musicians are not removed automatically when a unit breaks and flees from combat. Their instruments are somewhat lighter and less cumbersome than a weighty standard. Musicians cannot be captured as trophies.

A Musician model is placed in the front rank of its unit. His effect on the fighting ability of the unit is not as great as a Standard Bearer but is useful nonetheless.</description>
    </rule>
    <rule id="697c-46aa-691c-9c64" name="Champion (Warhammer Glossary)" hidden="false">
      <description>Champions are a special type of character who must always be with a unit. Champions must be placed in the front rank of the unit that they are with.</description>
    </rule>
    <rule id="1648-091e-ca90-e56d" name="Bow" hidden="false">
      <description>The bow, is carried by most races and used extensively in warfare. It is a compact, long-ranged weapon that is cheap to make and easy to maintain.

Bow Profile</description>
    </rule>
    <rule id="cd70-2ed2-922d-0011" name="Crossbow" hidden="false">
      <description>A crossbow consists of a short, strong bowstave mounted on a wooden or steel stock. It takes a long time to load and wind a crossbow for each shot, but the crossbow bolt has tremendous range and power.

Crossbow Profile</description>
    </rule>
    <rule id="dad4-d7e5-09e8-3819" name="Flail" hidden="false">
      <description>Rules: +2 Strength bonus in the first turn of combat; requires two hands.</description>
    </rule>
    <rule id="e020-fa73-42e2-ad20" name="Great Weapon" hidden="false">
      <description>Great weapons are especially large and heavy weapons that are wielded with both hands. As well as great swords this includes similarly heavy great hammer, great axes and the like. A blow from a great weapon can cut a foe in haIf and break apart the thickest armour.

Rules: +2 Strength bonus; requires two hands; strikes last.</description>
    </rule>
    <rule id="318c-0aad-5fdc-96c0" name="Halberd" hidden="false">
      <description>Rules: +1 Strength bonus; requires two hands.</description>
    </rule>
    <rule id="3eb5-f0b5-1e94-0eef" name="Hand Weapon" hidden="false">
      <description>Unless specifically noted otherwise, all models are assumed to be carrying a hand weapon of some kind. The term &apos;hand weapon&apos; is used to describe any weapon held in one hand and not otherwise covered by the rules. As such it includes swords. axes clubs, maces, etc.

Rules: No special weapon rules apply to hand weapons but they do have the advantage that they can be used in combination with each other (see Fighting with a Weapon in Each Hand) or with a shield (see Fighting with a Hand Weapon and Shield).</description>
    </rule>
    <rule id="9faf-8e95-aa25-b156" name="Handgun" hidden="false">
      <description>A handgun is a simple firearm consisting of a metal barrel mounted on a wooden stock. The gunpowder charge is ignited by poking a length of burning cord, or match as it is called, into a small touchhole. Some of the more advanced versions made by Dwarfs have levers and springs which hold the burning match and triggers which release the firing mechanism and fire the gun.

Handguns are not terribly reliable weapons, as occasionally the gun barrel tends to explode violently apart or the powder fails to ignite. Handguns, however, do have a long range and hit very hard, making a mockery of even the thickest armour.

Handgun Profile</description>
    </rule>
    <rule id="d8c8-edc7-35dd-2b4d" name="Javelin" hidden="false">
      <description>The javelin is a light spear designed for throwing, and javelin armed warriors often carry several to last them throughout the battle. The javelin is too flimsy to be used in hand-to-hand fighting. It is not a very common weapon as it has a short range, but the multitudinous reptilian skinks of Lustria use javelins extensively.

Javelin Profile</description>
    </rule>
    <rule id="7154-2d01-2d5c-c06c" name="Lance" hidden="false">
      <description>Rules: +2 Strength bonus in the first turn of combat when charging.</description>
    </rule>
    <rule id="c45c-2383-8be2-1152" name="Longbow" hidden="false">
      <description>A longbow is a dangerous weapon made of alternating layers of either yew or elm. A skilled archer can hit an enemy from three hundred paces.

Longbow Profile</description>
    </rule>
    <rule id="505c-f8fe-ee87-d4c3" name="Morning Star" hidden="false">
      <description>This is a single-handed weapon that consists of one or more spiked balls on a chain. Like the larger flail it resembles, a morning star is a tiring weapon to use so its advantage lies in the first round of combat.

Rules: +1 Strength bonus in the first turn of combat.</description>
    </rule>
    <rule id="11c6-d068-224a-5939" name="Repeater Crossbow" hidden="false">
      <description>Used almost exclusively by the Dark Elves of Naggaroth, the repeater crossbow is a lighter, less powerful type of crossbow that has a magazine of bolts which allows a single bolt to drop into place ready for firing as the string is drawn. A repeater crossbow can fire a hail of shots in the time it takes to shoot one ordinary crossbow bolt.

Repeater Crossbow Profile</description>
    </rule>
    <rule id="982a-e058-7b39-44d9" name="Sling" hidden="false">
      <description>\* If enemy is within 9&quot;</description>
    </rule>
    <rule id="6566-55b1-e8b7-d3d8" name="Throwing Axe" hidden="false">
      <description>Note that throwing axes cannot be used in close combat — or if used they simply count as hand weapons. Normal axes carried as hand weapons cannot be thrown either!

Throwing Axe Profile</description>
    </rule>
  </sharedRules>
  <sharedInfoGroups>
    <infoGroup id="3e93-6230-180b-9a1c" name="Swarm" hidden="false">
      <infoLinks>
        <infoLink id="c71f-2aa1-9f76-3b73" name="Unbreakable" hidden="false" targetId="f6c9-ac44-1d7c-ed6e" type="rule"/>
        <infoLink id="394a-fe0e-9c27-e1f9" name="Small" hidden="false" targetId="3783-e8d5-f94a-7b2c" type="rule"/>
        <infoLink id="7f72-3e5f-e5f6-c7e3" name="Swarm" hidden="false" targetId="21d5-5848-02a7-f995" type="rule"/>
      </infoLinks>
    </infoGroup>
  </sharedInfoGroups>
</gameSystem>