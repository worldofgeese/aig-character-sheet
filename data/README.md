# Extracted Mythras/RuneQuest Game Data

This directory contains game data extracted from the spreadsheet reference file and converted to JSON format for easy use in JavaScript applications.

## Files

### 1. skills.json (147 skills)
Contains all skills with their base stat pairs and starting bonuses.

**Structure:**
```json
{
  "name": "Athletics",
  "base_stats": ["STR", "DEX"],
  "starting_bonus": 0
}
```

**Key fields:**
- `name`: Skill name
- `base_stats`: Array of two stat abbreviations (STR, DEX, CON, SIZ, INT, POW, CHA)
- `starting_bonus`: Starting percentage bonus (0 for most skills, 30-40 for some)

### 2. weapons.json (358 weapons)
Contains all weapons with complete statistics.

**Structure:**
```json
{
  "name": "Broadsword",
  "weapon_type": "handweapon",
  "handedness": "1h",
  "damage": "1d8",
  "size": "M",
  "reach": "M",
  "offensive_special_effects": "Bleed,Impale",
  "armour_points": 6,
  "hit_points": 10,
  "encumbrance": 2
}
```

**Key fields:**
- `name`: Weapon name
- `weapon_type`: handweapon, ranged, firearms, etc.
- `handedness`: 1h, 2h, shield, ranged, unarmed
- `damage`: Damage dice formula
- `size`: S (Small), M (Medium), L (Large), H (Huge)
- `reach`: S (Short), M (Medium), L (Long), VL (Very Long), etc.
- `offensive_special_effects`: Comma-separated list of special effects
- `defensive_special_effects`: Comma-separated list (if applicable)
- `armour_points`: AP value
- `hit_points`: HP value
- `encumbrance`: ENC value
- `max_range`: For ranged weapons (format: "close/effective/extreme")
- `traits`: Additional weapon traits
- `description`: Detailed description (when available)

### 3. special-effects.json (44 effects)
Contains all combat special effects with their properties.

**Structure:**
```json
{
  "name": "Impale",
  "offensive": true,
  "defensive": false,
  "stackable": false,
  "specific_weapon_type": "Impaling Weapons"
}
```

**Key fields:**
- `name`: Effect name
- `offensive`: Boolean - can be used offensively
- `defensive`: Boolean - can be used defensively
- `stackable`: Boolean - can be stacked multiple times
- `specific_weapon_type`: Required weapon type (if applicable)
- `specific_roll`: Special roll requirement (if applicable)

### 4. combat-style-traits.json (106 traits)
Contains all combat style traits with explanations.

**Structure:**
```json
{
  "name": "Assassination",
  "explanation": "Allows the user access to the normally restricted 'Kill Silently' special effect."
}
```

**Key fields:**
- `name`: Trait name
- `explanation`: Full explanation of the trait's mechanics

### 5. runes.json (33 runes)
Contains all Gloranthan runes with complete metadata.

**Structure:**
```json
{
  "name": "Rune:Darkness",
  "short_name": "Darkness",
  "rune": "Darkness",
  "meaning": "Darkness, Cold, Underworld, Hunger, Insects",
  "personality_traits": "Cruel, Cold, Secretive, Patient",
  "rune_type": "Elemental",
  "metal": "Lead",
  "instrument": "Drum",
  "weapon": "Club",
  "tool": "Hammer",
  "action": "Conceal",
  "color": "Purple",
  "direction": "Below",
  "emotion": "Fear",
  "fauna": "Insects",
  "flesh": "Fat",
  "flora": "Fungi",
  "organ": "Stomach",
  "sense": "Hearing",
  "stone": "Obsidian"
}
```

**Key fields:**
- `name`: Full rune name (format: "Rune:Name")
- `short_name`: Short name
- `rune`: Rune identifier
- `meaning`: Description of what the rune represents
- `personality_traits`: Associated personality traits
- `rune_type`: Form, Elemental, Power, or Condition
- Additional fields: metal, instrument, weapon, tool, action, color, direction, emotion, fauna, flesh, flora, organ, sense, stone (when applicable)

### 6. equipment.json (65 items)
Contains general equipment with encumbrance values.

**Structure:**
```json
{
  "name": "Backpack/Satchel",
  "encumbrance": 1
}
```

**Key fields:**
- `name`: Equipment name
- `encumbrance`: ENC value (omitted if '-' or negligible)

## Usage

All files are standard JSON and can be imported directly into JavaScript:

```javascript
import skills from './data/skills.json';
import weapons from './data/weapons.json';
import specialEffects from './data/special-effects.json';
import combatStyleTraits from './data/combat-style-traits.json';
import runes from './data/runes.json';
import equipment from './data/equipment.json';
```

## Data Source

Extracted from: `/tmp/aig-character-sheet/references/spreadsheet-extract.txt`

The extraction was performed exhaustively to capture all available data from the spreadsheet.

## Notes

- All JSON files are formatted with 2-space indentation for readability
- String values preserve original formatting from the spreadsheet
- Numeric values (AP, HP, ENC) are converted to integers where possible
- Missing or optional fields are omitted rather than set to null
- Some fields may contain special characters (\\xa0 for non-breaking spaces)
