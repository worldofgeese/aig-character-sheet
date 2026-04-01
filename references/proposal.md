# Adventures in Glorantha — Hyperclay Character Sheet

## Why
The only existing character sheet tool for Adventures in Glorantha (AiG) is a Google Sheets/Excel template (V1.06). It works, but it's not new-player-friendly — it dumps you into a flat spreadsheet with no guidance on the *order* of character creation steps, no page references to the AiG or Mythras books, and no mobile support. The RQ Wiki (rqwiki.chaosium.com) showed what a step-driven character creator looks like for RuneQuest — we want that for AiG/Mythras.

## What
A single self-contained Hyperclay HTML file that:
1. **Step-driven wizard** for character creation (like the RQ Wiki flow)
2. **Page references** to Adventures in Glorantha and Mythras Core Rulebook for every step
3. **New-player friendly** — explains concepts inline, guides choices
4. **Perfect mechanical fidelity** — every formula from the spreadsheet, faithfully ported to JS
5. **Compact play mode** — after creation, collapses into a usable character sheet
6. **Mobile-friendly** — responsive, touch-optimized

## Spreadsheet Architecture (extracted from V1.06)

### 12 Sheets
| Sheet | Purpose |
|-------|---------|
| HOW TO USE and About | Instructions |
| **datasheet** | PRIMARY INPUT: all player-entered values live here |
| **PAGE 1** | Character record sheet — skills, combat, hit locations |
| **PAGE 2** | Spells, rune affinities, equipment, notes |
| **PAGE 3** | Spirit/Sorcery magic details |
| **CULTS** | Up to 12 cult slots (4 groups × 3) with rank/title/devotional pool |
| **calculations** | Damage mod table, equipment list, size chart, encumbrance, difficulty mods, careers/races, age→bonus points |
| **Calculations-Skills** | 147 skills with their base stat pairs (STR+DEX, INT+POW, etc.) and starting bonuses |
| **Runes** | 33 Gloranthan runes with personality traits, metals, elements |
| **Special Effects Summary** | Combat special effects reference |
| **Calculations-CombatStyleTraits** | Combat style trait reference |
| **Calculations-Weapons** | 360 weapons with stats, damage, size, reach, traits, AP/HP |

### Key Formulas (Mythras Engine)
```
Action Points = ROUNDUP((DEX + INT) / 12, 0)
Experience Modifier = ROUNDUP(CHA / 6, 0) - 2
Healing Rate = ROUNDUP(CON / 6, 0)
Luck Points = ROUNDUP(POW / 6, 0)
Magic Points = POW
Initiative Bonus = ROUNDUP(AVERAGE(DEX, INT), 0)
Damage Modifier = VLOOKUP(CEILING((STR + SIZ) / 5, 1), damage_table)

HP per Location (humanoid):
  Head = ROUNDUP((CON + SIZ) / 5, 0)
  Chest = ROUNDUP((CON + SIZ) / 5, 0) + 2
  Abdomen = ROUNDUP((CON + SIZ) / 5, 0) + 1
  Arm = MAX(ROUNDUP((CON + SIZ) / 5, 0) - 1, 1)
  Leg = ROUNDUP((CON + SIZ) / 5, 0)

Skill Base = Stat1 + Stat2 + starting_bonus
Skill Total = base + culture + career + bonus + other

Encumbrance:
  Unencumbered = STR × 2
  Burdened = (STR × 2) + 1
  Overloaded = (STR × 3) + 1
  No movement = STR × 4
```

### Age → Bonus Points
| Age Range | Category | Bonus Points | Max per Skill | Background Events |
|-----------|----------|-------------|---------------|-------------------|
| 12-16 | Young | 100 | 10 | 0 |
| 17-27 | Adult | 150 | 15 | 1 |
| 28-42 | Middle Aged | 200 | 20 | 2 |
| 43-57 | Senior | 250 | 25 | 3 |
| 58+ | Old | 300 | 30 | 4+ |

### Point Budgets
- Culture Points: 100 (distributed across standard + professional skills)
- Career Points: 100 (distributed across standard + professional + magic skills)
- Bonus Points: age-dependent (see above)

### Data Validation (Dropdowns)
- Culture: Primitive, Barbarian, Civilised, Nomad
- Social Class: Outcast, Slave, Freeman, Gentry, Aristocracy, Ruling
- Frame: Lithe, Medium, Heavy
- Handedness: Right, Left, Ambi.
- Difficulty Mod: Very Easy, Easy, Standard, Hard, Formidable, Herculean

### Races (with characteristic dice)
Humans (3d6 each, 2d6+6 SIZ/INT), Dwarf, Elf, Gnome, Half-Elf, Half-Orc, Halfling, Minotaur, Centaur, Iqari, Satyr, Nymph

### 33 Gloranthan Runes
Elemental (Air/Storm, Darkness, Earth, Fire/Sky, Water, Moon), Power (Death/Fertility, Harmony/Disorder, Movement/Stasis, Truth/Illusion), Form (Beast, Chaos, Dragon, Dragonewt, Man, Plant, Spirit), Condition (Cold, Dragon, Eternal Battle, Fate, Infinity, Law, Light, Luck, Magic, Mastery, Power, Trade, Unlife)

### Cult System
12 cult slots across 4 groups. Each cult has:
- Name, Type (Theist/Animist/Sorcery/Mystical/Brotherhood)
- Rank hierarchy (5 levels per type)
- Benefits, Restrictions, Geasa, Gifts
- Devotional Pool = f(rank, POW, cult_type)
- Magic Points pool tracking

## Open Questions for Tao

1. **Which AiG edition/version?** I need the PDF to extract page numbers.
2. **Mythras Core Rulebook — which edition?** Same reason.
3. **Character creation step order:** The spreadsheet implies Culture → Race → Characteristics → Skills → Career → Passions → Magic/Runes → Cults → Equipment. Is this the AiG book's order?
4. **Scope of "character creator" vs "character sheet":** Should the wizard include *all* possible choices (e.g., picking from the 360-weapon list), or just the mechanical framework with blank slots for manual entry?
5. **Rune Magic integration:** The spreadsheet has Rune skills (Rune:Cold, Rune:Darkness, etc.) with base = POW×2 + other. These are Glorantha-specific additions to Mythras. How deep should the rune magic section go?
6. **Cult selection:** Should we have a searchable cult database, or free-text cult entry like the spreadsheet?
7. **Special Effects reference:** Include in the sheet, or separate reference page?
