# Fix Brief: Remaining prompt() calls and mobile polish

## Issues

### 1. Three prompt() calls still remain (lines 1345, 1564, 1662)
- `App.addCustomPassion()` — uses `prompt('Passion name:')`
- `App.addCareerSkill()` — uses `prompt('Skill name:')`  
- `App.addBonusSkill()` — uses `prompt('Skill name:')`

All three should use inline text inputs with autocomplete, matching the pattern already established for weapons/armor/equipment in `createAutocomplete()`.

### 2. Mobile Remove button verification
The @media breakpoint exists and uses grid (not flex-wrap). Grid `1fr` layout should stack elements properly. But `.skill-row` doesn't have explicit grid columns defined outside the media query — check that the Remove button is visible at all viewport widths.

## Fix Pattern

For each prompt() call, replace with an inline text input that:
- Appears below the "+" button when clicked  
- Has a text input + "Add" button side by side
- For skills: show autocomplete suggestions from standard/professional skill lists
- For passions: show autocomplete from PASSION_TYPES or free text

### Data sources for autocomplete:
- **Passions:** The passion types from Mythras — "Loyalty to X", "Love (X)", "Hate (X)", "Devotion to X", "Fear of X"
- **Career skills:** All Professional Skills + Combat Styles (these are the valid hobby skills)
- **Bonus skills:** Same as career skills (professional + combat styles)

## Constraints
- Must work on mobile (touch targets ≥44px)
- Must be keyboard navigable
- Inline pattern (no modal/dialog)
- Don't break existing autocomplete for weapons
