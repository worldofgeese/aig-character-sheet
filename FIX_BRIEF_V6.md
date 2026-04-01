# Fix Brief: Mobile UX + Validation + Equipment Costs + Pocketfold (v5)

## Branch
Work on branch `fix/v5-mobile-validation-pocketfold`. Do NOT merge to main.

## Issues (7 bugs)

### Bug 1: Hit points by location doesn't fit on mobile
The body diagram SVG + hit location table side by side overflows on narrow screens. Fix: Stack vertically on mobile. Add `@media (max-width: 600px)` rule to make the body diagram and table full-width and stacked.

### Bug 2: Suggested character builds hidden behind clickable collapsible  
The "💡 Suggested Character Builds for [Culture]" is a collapsible that must be clicked to expand. New players might not realize it's clickable. Fix: Remove the collapsible wrapper and show all suggested builds by default, always visible when a culture is selected.

### Bug 3: Step 8 allows advancing without selecting 3 professional skills
The "Professional Skills (choose 3)" checkboxes don't block advancement if fewer than 3 are selected. Fix: Add validation in `validateCurrentStep()` for step 8:
```js
if (step === 8) {
  if (!CharacterData.career) { ... }
  const selected = (CharacterData.selectedProfessionalSkills || []).length;
  if (selected < 3) {
    this.showToast('You must select exactly 3 professional skills', 'error');
    return false;
  }
}
```

### Bug 4: Skill tooltips cramped on mobile
The ℹ️ tooltip text is colliding with skill input boxes on mobile. Fix: On mobile, position tooltips below the element instead of above, and make them full-width:
```css
@media (max-width: 600px) {
  .skill-tooltip .tooltip-text {
    position: fixed;
    left: 10px;
    right: 10px;
    bottom: auto;
    top: auto;
    width: auto;
    transform: none;
    z-index: 9999;
  }
}
```

### Bug 5: Equipment shows AP:0 HP:0 instead of actual weapon stats
In the screenshot, Broadsword shows "(1d8, AP:0 HP:0)" — the `addWeapon` function reads `weapon.armour_points` but the pushed object uses `ap: weapon.armour_points || 0`. The issue is the weapon was added but the rendering shows AP:0 HP:0. Check the rendering code — it might be reading `w.armour_points` instead of `w.ap`. Fix: Ensure consistent property names in both storage and rendering.

### Bug 6: Equipment/weapons/armor don't show costs in autocomplete
The autocomplete dropdown only shows weapon names. Fix: Update the `createAutocomplete` function to show stats in the dropdown:
- Weapons: `Broadsword (1d8, AP:6 HP:10, Size:M)`
- Armor/shields: `Heater Shield (AP:6 HP:12, Size:L)`
- Equipment: `Rope, hemp 10m (ENC:2)`

Check if the worker from v2 actually implemented this — the brief asked for it but the screenshots show it's not working.

### Bug 7: Print Pocketfold button does nothing when clicked
The `printPocketfold()` function exists but doesn't work. Debug: check if the function properly generates the pocketfold view, populates the panels, and triggers print. The function might be failing silently because it can't find the pocketfold HTML elements.

### Bug 8: Top row buttons collide on mobile
The button bar (Wizard Mode, Play Mode, Print, Print Pocketfold, Save, Load) all collide on narrow screens. Fix: Wrap the buttons using `flex-wrap: wrap` and add gap:
```css
.no-print { 
  display: flex; 
  flex-wrap: wrap; 
  gap: 5px; 
  justify-content: flex-end;
}
```

## Testing
1. `python3 -m unittest tests.test_calculations -v` must pass
2. Commit with descriptive message
3. Push to branch, do NOT merge
