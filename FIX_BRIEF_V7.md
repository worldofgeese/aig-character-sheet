# Fix Brief: RAW Compliance, Trademark, and UI Overhaul (v6)

## Branch
Work on branch `fix/v6-raw-compliance`. Do NOT merge to main.

## Priority: CRITICAL — Rules Compliance

These changes are about making the character sheet follow the Rules As Written (RAW) from the Mythras Core Rulebook. This is not optional polish — incorrect rules implementation makes the tool useless.

---

## Bug 1: Passion skills showing in the skills table (SCREENSHOT)
The skills "A concept or ideal", "A person in a platonic context...", etc. are PASSIONS, not skills. They should NOT appear in the main skills list in Play Mode. They have a `starting_bonus: 30` in SKILLS_DATA which makes them look like skills, but they're passion categories.

**Fix:** Filter out passion-category entries from the skills display. Passions start with "A " or "An " in the SKILLS_DATA. Remove them from the main skill table rendering in Play Mode. They should only appear in the Passions section.

## Bug 2: Combat weapons display broken on mobile (SCREENSHOT)
The weapon table in Play Mode shows each stat (Skill, Damage, Size, Reach, AP, HP) on its own line instead of in a grid/table row. The layout is completely broken on mobile.

**Fix:** Use a compact table or horizontal scroll for the weapons display. On mobile, show a card layout per weapon instead of a broken table.

## Bug 3: Special Effects has double arrow "► ►"
The collapsible header shows two arrows.

**Fix:** Remove the duplicate arrow. Should be just "▶ Special Effects Reference (44 effects)".

## Bug 4: Homeland should be autocompletable
Currently a free text field. Should offer suggestions based on the selected culture.

**Data:**
- Balazaring: Balazar, Elder Wilds, Votankiland
- Esrolian: Nochet, Esrolia, Ezel
- God Forgot: God Forgot, Holy Country
- Lunar Heartland: Glamour, Alkoth, Raibanth, Yuthuppa
- Praxian: Prax, The Wastes, Pavis County
- Provincial Lunar/Tarsh: Furthest, Alda-Chur, Dunstop
- Sartarite/Heortling: Boldhome, Jonstown, Clearwine, Apple Lane
- Telmori Hsunchen: Telmori Wilds, Sartar borders

**Fix:** Add a datalist with culture-specific homeland suggestions. Keep the input as free text (player can type anything) but offer suggestions.

## Bug 5: Suggested Character Builds should auto-fill when clicked
Currently builds show stat recommendations as text. They should be clickable buttons that:
1. Show a confirmation dialog: "This will set your characteristics, career, and combat style. Continue?"
2. If confirmed, set CharacterData.characteristics to the recommended values
3. Set the recommended career
4. Pre-select the recommended combat style
5. Show a toast confirming what was changed

## Bug 6: "Combat Style (Cultural Style)" is unclear
New players don't know what this means. 

**Fix:** When displaying combat styles in the skills list, append the actual combat style NAME from the culture data. For example, if the culture is Praxian, "Combat Style (Cultural Style)" should show as "Combat Style (Beast Rider Warrior)" or whichever style the player has chosen.

## Bug 7: Step 10 Bonus Points should show total modified skill
Currently shows just the bonus points allocated. Should show: `Base + Culture + Career + Bonus = Total`

**Fix:** In renderStep10, for each skill row, show the computed total after bonus points are added. E.g., "Influence: 24 base + 30 culture + 0 career + 15 bonus = 69%"

## Bug 8: Remove Step 11 (Equipment) — auto-add starting equipment
Per Mythras RAW, characters get starting equipment based on their career. Remove the entire Step 11 from the wizard. Instead, auto-populate equipment in Play Mode based on the career's standard starting gear.

**Implementation:**
- Remove renderStep11 from the wizard
- Change wizard to 11 steps (renumber Step 12 to Step 11)
- In Play Mode, auto-add starting equipment based on career
- Keep the equipment section in Play Mode editable (add/remove items)
- Update all step references and validation

## Bug 9: Editable number under weapons in Play Mode is unclear
The editable number field under each weapon in Actions/Combat is meant to represent... what? Skill percentage? Current AP? 

**Fix:** Label it clearly. If it's the combat skill percentage, label it "Skill %" and pre-fill from the character's combat style skill value.

## Bug 10: Point-buy allows too many points per skill
Cultural and career skill distribution allows putting all 100 points into one skill. 

**RAW Fix (Mythras p.13, p.28):**
- Cultural skills: each skill can receive a maximum of **15 points** from cultural distribution
- Career skills: each skill can receive a maximum of **15 points** from career distribution
- The per-skill max should be enforced in the input fields and validation

Wait — actually check the RAW carefully. The limits might be different. Mythras p.13 says the 100 points for cultural skills can be distributed "as desired." The actual limit is that you can only add to skills that come with your culture/career — not ALL skills. Let me clarify:

**Actual RAW constraints:**
- Cultural Skills (Step 5): Distribute 100 points ONLY among the skills listed for your culture. You cannot add to skills not in the culture list.
- Career Skills (Step 9): Distribute 100 points ONLY among the skills listed for your career. You cannot add to skills not in the career list.
- Bonus Points (Step 10): Can add to ANY skill already on your sheet (cultural + career skills), plus ONE additional professional skill as a hobby.

**Fix:** 
- Step 5: Only show the culture's listed skills for point distribution (already does this)
- Step 9: Only show the career's listed skills for point distribution
- Remove the "Add Skill" button from Steps 5 and 9 — players can only distribute among the listed skills
- Step 10: Allow adding exactly 1 hobby professional skill

## Bug 11: Professional skills in Play Mode should only show selected ones
Currently ALL professional skills show with base percentages. Only the professional skills the player selected (from culture + career + 1 hobby) should appear.

**Fix:** In Play Mode skill display, filter professional skills to only show:
- Standard skills that have culture/career/bonus points added
- Professional skills that were selected during character creation
- All standard skills at their base values (these are always available)

Actually per RAW: ALL standard skills appear (at base or modified). Only SELECTED professional skills appear (the ones from culture + career + hobby). Professional skills not selected don't appear at all.

## Bug 12: Add trademark statements

Add the following to the bottom of the character sheet (visible in both Play Mode and print):

**Design Mechanism:**
"Mythras" and "Mythras Imperative" are Registered Trademarks of The Design Mechanism Inc, and are used with permission.

**Chaosium:**
This tool uses trademarks and/or copyrights owned by Chaosium Inc/Moon Design Publications LLC, which are used under Chaosium Inc's Fan Material Policy. We are expressly prohibited from charging you to use or access this content. This tool is not published, endorsed, or specifically approved by Chaosium Inc. For more information about Chaosium Inc's products, please visit www.chaosium.com.

---

## Implementation Order
1. Bug 12 (trademark) — add immediately, this is a legal requirement
2. Bug 10 (point-buy limits) — RAW compliance
3. Bug 11 (professional skills filtering) — RAW compliance
4. Bug 8 (remove Step 11) — RAW compliance
5. Bug 1 (passion skills filtering) — display fix
6. Bug 2 (weapon display mobile) — layout fix
7. Bug 3 (double arrow) — cosmetic
8. Bug 4 (homeland autocomplete) — UX
9. Bug 5 (build auto-fill) — UX
10. Bug 6 (combat style names) — clarity
11. Bug 7 (bonus point totals) — clarity
12. Bug 9 (weapon number label) — clarity

## Testing
1. `python3 -m unittest tests.test_calculations -v` must pass
2. Verify trademark text appears at bottom of sheet
3. Verify passions don't appear in skills table
4. Verify only selected professional skills appear
5. Commit and push to branch, do NOT merge
