# Fix Brief: Validation, Equipment Display & Money System

## Branch
Work on branch `fix/v2-validation-equipment`. Do NOT merge to main.

## Issues (7 bugs)

### Bug 1: Steps allow advancing without spending all points
**Steps affected:** 5 (cultural skills), 9 (career skills), 10 (bonus points)

Current validation only checks for *overspending*. It needs to also require minimum spending:
- Step 5: Must spend exactly 100 cultural skill points (currently allows 0/100)
- Step 9: Must spend exactly 100 career skill points (currently allows 0/100)  
- Step 10: Must spend all bonus points for the age category (currently allows 0/150)

**Fix:** In `validateCurrentStep()`, add underspending checks:
```js
if (step === 5) {
  if (spent !== 100) { // was: spent > 100
    this.showToast('You must distribute exactly 100 cultural skill points', 'error');
    return false;
  }
}
// Same pattern for steps 9 and 10
```

### Bug 2: Added equipment/weapons/armor don't display in Step 11
The `renderStep11` function creates empty `#weapons-list`, `#armor-list`, `#equipment-list` divs but never renders existing items from `CharacterData.weapons`, `CharacterData.armor`, `CharacterData.equipment`.

**Fix:** After creating the div, populate each list with existing items:
```js
// After div.innerHTML = ...
const weaponsList = div.querySelector('#weapons-list');
CharacterData.weapons.forEach((w, i) => {
  const row = document.createElement('div');
  row.className = 'skill-row';
  row.innerHTML = `
    <span>${w.name} (${w.damage}, AP:${w.ap} HP:${w.hp})</span>
    <button onclick="CharacterData.weapons.splice(${i},1); App.saveToLocalStorage(); App.renderCurrentStep()">Remove</button>
  `;
  weaponsList.appendChild(row);
});
// Same for armor and equipment
```

### Bug 3: No "Roll Starting Money" button
The starting money formula is shown as text (e.g. "4d6×15 Lunars") but there's no way to roll it.

**Fix:** Parse the formula and add a Roll button:
```js
<button onclick="App.rollStartingMoney()">🎲 Roll Starting Money</button>
```

`App.rollStartingMoney` should:
1. Parse the culture's `startingMoney` string (format: "4d6×N Lunars" or "4d6×N")
2. Roll 4d6 (sum of 4 random d6 rolls)
3. Multiply by the multiplier
4. Set `CharacterData.startingMoney` to the result
5. Re-render the step

### Bug 4: Equipment costs not shown in autocomplete
The autocomplete dropdown shows only weapon/equipment names. It should show cost where available.

**Fix:** The WEAPONS_DATA and EQUIPMENT_DATA don't have price fields (Mythras doesn't standardize equipment prices in the core book). Instead, show the key stats:
- Weapons: show `name (damage, size, AP:X HP:Y)`  
- Armor/shields: show `name (AP:X HP:Y, size)`
- Equipment: show `name (ENC:X)` if encumbrance > 0

Update `createAutocomplete` item rendering:
```js
results.innerHTML = matches.map(item => {
  let detail = '';
  if (item.damage) detail = `${item.damage}, AP:${item.armour_points||0} HP:${item.hit_points||0}`;
  else if (item.encumbrance) detail = `ENC:${item.encumbrance}`;
  return `<div class="autocomplete-item" data-name="${item.name}">
    ${item.name}${detail ? ' <span style="color:#888">(' + detail + ')</span>' : ''}
  </div>`;
}).join('');
```

### Bug 5: Adding items doesn't subtract from money
When adding weapons/armor/equipment, no cost is subtracted from `CharacterData.startingMoney`.

**Fix:** Since WEAPONS_DATA doesn't include prices, we can't auto-subtract. Instead:
- Show a "Cost" input field next to each added item
- When cost is entered, subtract from starting money and update display
- Store cost on each item: `CharacterData.weapons[i].cost = X`
- Current Money = startingMoney - sum(all item costs)

### Bug 6: Step 12 (Review) doesn't show equipment/weapons/armor
The character complete summary needs to list all equipment.

**Fix:** In `renderStep12`, add sections for weapons, armor, and equipment.

### Bug 7: Step 1 has no validation
Name and concept can be empty. Add basic validation requiring at least a character name.

## Implementation Order
1. Bug 1 (validation) — quick fix in validateCurrentStep
2. Bug 7 (step 1 validation) — quick add
3. Bug 2 (equipment display) — render existing items
4. Bug 3 (roll money) — add roll button + parser
5. Bug 5 (cost tracking) — add cost field + auto-calculate
6. Bug 4 (autocomplete stats) — update item rendering
7. Bug 6 (step 12 review) — add equipment to summary

## Testing
After all fixes:
1. Run `python3 -m unittest tests.test_calculations -v` — must still pass
2. Manual check: try advancing past Step 5 with 0/100 points → should be blocked
3. Manual check: add a weapon in Step 11 → should show in the list
4. Manual check: roll money → should populate the money field
5. Commit with descriptive message, push to branch

## Constraints
- Single HTML file — all changes in aig-character-sheet.html
- Must work on mobile (touch targets ≥44px)
- Don't break existing autocomplete or any other step
- Use `parseInt(value) || 0` pattern for all number inputs (prevent NaN)
