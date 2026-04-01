# AiG Character Sheet — Build Task Brief

## Objective
Build a single self-contained Hyperclay HTML character sheet for Adventures in Glorantha (Mythras engine). 12-step character creation wizard + play mode. All formulas ported from the V1.06 Excel spreadsheet.

## Repo
`/tmp/aig-character-sheet/`

## Deliverable
`aig-character-sheet.html` — single Hyperclay HTML file

## Design Spec
Read `/home/node/.openclaw/workspace/projects/aig-character-sheet/openspec/changes/glorantha-character-sheet/design.md` for full design decisions.

Read `/home/node/.openclaw/workspace/skills/hyperclay/SKILL.md` for Hyperclay conventions.

## Reference Data (already extracted)
- Full spreadsheet extraction: `/tmp/aig_full_extract.txt` (10,064 lines)
- AiG character creation chapter: `/tmp/aig_chars.txt`
- Mythras character creation chapter: `/tmp/mythras_char_creation.txt`
- AiG page reference map: `/home/node/.openclaw/workspace/projects/aig-character-sheet/references/aig-page-map.md`
- Mythras page reference map: `/home/node/.openclaw/workspace/projects/aig-character-sheet/references/mythras-page-map.md`
- Proposal with full formula documentation: `/home/node/.openclaw/workspace/projects/aig-character-sheet/openspec/changes/glorantha-character-sheet/proposal.md`

## Key Design Decisions
1. **Human only** — no non-human races
2. **Both point-buy (75pts, default) and dice rolling** (3d6 / 2d6+6)
3. **Auto-fill** cultural data on culture selection (skills, combat styles, folk magic, passions)
4. **Hard enforcement** on point budgets — can't proceed if overspent
5. **360-weapon searchable database** with autocomplete
6. **Special effects summary** (41 effects) embedded as collapsible panel
7. **Difficulty modifier** dropdown in play mode
8. **A4 portrait print** + **pocketfold booklet** option
9. **~20 common Dragon Pass cults** embedded as JSON, free-text for exotic cults

## Character Creation Steps (from AiG p.23-24)
1. Concept — free text
2. Characteristics — 7 stats (STR/CON/SIZ/DEX/INT/POW/CHA), point-buy or dice
3. Attributes — auto-calculated from characteristics
4. Culture & Homeland — dropdown, 8 cultures
5. Cultural Skills & Magic — 100 culture points + rune affinities + folk magic
6. Passions — culture-specific starters
7. Background Details — optional
8. Career — culture-filtered list
9. Career Skills & Magic — 100 career points + 2 folk magic spells
10. Age & Bonus Points — age-dependent
11. Equipment & Money — culture-based starting money
12. Review & Play — transition to play mode

## Core Formulas (from spreadsheet)

### Attributes (from datasheet B19:D26)
```javascript
actionPoints = Math.ceil((DEX + INT) / 12)
experienceModifier = Math.ceil(CHA / 6) - 2
healingRate = Math.ceil(CON / 6)
luckPoints = Math.ceil(POW / 6)
magicPoints = POW
initiativeBonus = Math.round((DEX + INT) / 2)

// Damage Modifier lookup (STR+SIZ combined, divided by 5, ceiling)
const DAMAGE_MOD_TABLE = {
  1: '-1d8', 2: '-1d6', 3: '-1d4', 4: '-1d2', 5: '0',
  6: '1d2', 7: '1d4', 8: '1d6', 9: '1d8', 10: '1d10',
  11: '1d12', 12: '1d12', 13: '2d6', 14: '2d6',
  15: '1d8+1d6', 16: '1d8+1d6', 17: '2d8', 18: '2d8',
  19: '1d10+1d8', 20: '1d10+1d8'
}
damageModifier = DAMAGE_MOD_TABLE[Math.ceil((STR + SIZ) / 5)]
```

### Hit Points per Location (humanoid, from datasheet B28:C33)
```javascript
const base = Math.ceil((CON + SIZ) / 5)
hitPoints = {
  head: base,
  chest: base + 2,
  abdomen: base + 1,
  arm: Math.max(base - 1, 1),  // each arm
  leg: base                      // each leg
}
```

### Encumbrance (from calculations A57:B60)
```javascript
encumbrance = {
  unencumbered: STR * 2,
  burdened: STR * 2 + 1,
  overloaded: STR * 3 + 1,
  noMovement: STR * 4
}
```

### Skill Base Values
Each skill has two governing characteristics + optional starting bonus.
Full list in Calculations-Skills sheet (147 skills). Examples:
```javascript
// Standard Skills (base = stat1 + stat2 + bonus)
Athletics: STR + DEX
Boating: STR + CON
Brawn: STR + SIZ
Conceal: DEX + POW
Customs: INT + INT + 40  // always +40 starting bonus
Dance: DEX + CHA
Endurance: CON + CON
Evade: DEX + DEX
Willpower: POW + POW
// ... etc

// Skill total = base + culture + career + bonus + other
```

### Age → Bonus Points (from calculations N146:R224)
```javascript
const AGE_TABLE = [
  { min: 12, max: 16, category: 'Young', bonusPoints: 100, maxPerSkill: 10, bgEvents: 0 },
  { min: 17, max: 27, category: 'Adult', bonusPoints: 150, maxPerSkill: 15, bgEvents: 1 },
  { min: 28, max: 42, category: 'Middle Aged', bonusPoints: 200, maxPerSkill: 20, bgEvents: 2 },
  { min: 43, max: 57, category: 'Senior', bonusPoints: 250, maxPerSkill: 25, bgEvents: 3 },
  { min: 58, max: 999, category: 'Old', bonusPoints: 300, maxPerSkill: 30, bgEvents: 4 }
]
```

### Difficulty Modifiers (from calculations A63:B68)
```javascript
const DIFFICULTY_MODS = {
  'Very Easy': 2.0,
  'Easy': 1.5,
  'Standard': 1.0,
  'Hard': 0.66,
  'Formidable': 0.5,
  'Herculean': 0.1
}
// Applied skill = Math.ceil(skillTotal * modifier)
```

### Rune Affinities (AiG p.24)
```javascript
// Three runes, assigned in order:
// Primary: POW × 2 + 30
// Secondary: POW × 2 + 20
// Tertiary: POW × 2 + 10
// Base for individual rune skills: POW × 2 + other
```

### Folk Magic (AiG p.24)
```javascript
// Folk Magic skill base = POW + CHA + 30
// Characters start with 3 Folk Magic spells from culture list
// Career adds 2 more spells
```

### Devotional Pool (from CULTS sheet)
```javascript
// Only for Theist cults
function devotionalPool(rank, currentPOW) {
  switch(rank) {
    case 'High Priest': return Math.ceil(currentPOW)
    case 'Priest': return Math.ceil(currentPOW * 0.75)
    case 'Acolyte': return Math.ceil(currentPOW * 0.5)
    case 'Initiate': return Math.ceil(currentPOW * 0.25)
    case 'Lay Member': return 0
    default: return 0
  }
}
```

## AiG Cultures Data (from AiG p.25-41)
Embed these 8 cultures with their full skill lists, combat styles, folk magic, and passions:

### Balazaring (Primitive)
- Standard Skills: Athletics, Brawn, Endurance, Evade, Locale, Perception, Stealth, Boating or Swim
- Professional Skills: Craft (any), Healing, Lore (any), Musicianship, Navigate, Survival, Track
- Combat Styles: Hunter Raider (Spear, Bow, Sling; Skirmisher), Pony Cavalry (Spear, Bow; Mounted), Hawk Slayer (Longspear; Mounted)
- Folk Magic: Beastcall, Bladesharp, Cleanse, Coordination, Deflect, Dry, Find Game, Ignite, Mobility, Speedart
- Passions: Loyalty to Clan, Loyalty to City, Love or Hate
- Starting Money: 4d6×2 Lunars
- Careers: All Primitive

### Esrolian (Civilised)
- Standard Skills: Conceal, Deceit, Drive, Influence, Insight, Locale, Perception, Willpower
- Professional Skills: Art (any), Commerce, Craft (any), Courtesy, Language (any), Lore (any), Musicianship, Streetwise
- Combat Styles: Citizen Legionary (Shortsword, Shield, Javelin, Sling; Formation Fighting), City-State Phalangite (Longspear/Sarissa, Bow; Formation Fighting), Clan Protector (Shortsword, Shield, Shortspear; Daredevil)
- Folk Magic: Alarm, Appraise, Bladesharp, Calculate, Calm, Glamour, Heal, Lock, Perfume, Repair
- Passions: Loyalty to Clan (POW+CHA+30), Loyalty to Grandmother (POW+CHA+50), Loyalty to Queen (POW+CHA+25)
- Starting Money: 4d6×15 Lunars
- Careers: All Civilised

(Remaining 6 cultures to be extracted from /tmp/aig_chars.txt — God Forgot, Lunar Heartland, Praxian, Provincial Lunar/Tarsh, Sartarite/Heortling, Telmori Hsunchen)

## Careers (from calculations A31:A54)
Agent, Alchemist, Beast Handler, Courtesan, Courtier, Crafter, Entertainer, Farmer, Fisher, Herder, Hunter, Merchant, Miner, Mystic, Official, Physician, Priest, Sailor, Scholar, Scout, Shaman, Sorcerer, Thief, Warrior

## What NOT to include in v1
- Non-human races
- Cult database (cult slots are free-text in v1)
- Pocketfold print (A4 portrait first, pocketfold in v2)
- Background events tables (reference page number only)

## File Structure in Repo
```
aig-character-sheet/
├── README.md
├── aig-character-sheet.html    ← THE deliverable
├── scripts/
│   └── mythras_calculations.py ← verification script
├── data/
│   ├── skills.json             ← 147 skills with stat pairs
│   ├── weapons.json            ← 360 weapons
│   ├── equipment.json          ← equipment + ENC
│   ├── runes.json              ← 33 runes
│   ├── cultures.json           ← 8 AiG cultures
│   ├── careers.json            ← 24 careers
│   ├── special-effects.json    ← 41 combat special effects
│   └── combat-style-traits.json
├── tests/
│   └── test_calculations.py    ← verify against spreadsheet
└── references/
    ├── aig-page-map.md
    └── mythras-page-map.md
```

The JSON files are used during development/testing. In the final HTML, all data is embedded as JS constants inside `<script>` blocks.
