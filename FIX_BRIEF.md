# Fix Round: v1 UX Issues + Career Skills Data

## Branch
`fix/v1-ux-issues` (from `main`)

## Issues to Fix (all in `aig-character-sheet.html`)

### 1. Weapon/Armour/Equipment Search — Replace prompt() with inline autocomplete
**Current**: Uses `prompt()` dialog box — can't search, terrible UX especially on mobile.
**Fix**: Replace with an inline text input + filtered dropdown that shows matches as you type. When user types "Broad", show Broadsword, Broad Axe 1H, Broad Axe 2H. Click to add with auto-filled stats. Apply same pattern to armour and equipment if they use prompt() too.

### 2. Remove Button Cut Off on Mobile
**Current**: Remove/delete buttons overflow on narrow screens.
**Fix**: Ensure all row layouts wrap properly on mobile (≤600px). Remove buttons should be visible and tappable. Use `flex-wrap: wrap` or put the remove button on its own row at small breakpoints.

### 3. Bonus Points (Step 10) — Pre-populate with accumulated skills
**Current**: Shows empty "+ Add Skill" entries — user has to re-enter skills manually.
**Fix**: When entering Step 10, automatically populate the list with ALL skills the character has gained so far from culture (Step 5) and career (Step 9), showing their current totals. The player then distributes bonus points among these existing skills. Also allow adding ONE new Professional Skill or Combat Style as a hobby skill (per Mythras p.32). Enforce the age-category per-skill cap (10/15/20/25/30).

### 4. Career Skills — Add full skill lists + auto-populate on career selection
**Current**: Career skill lists are empty in `CAREERS_DATA`. Player has to manually enter skills.
**Fix**: 
a) Populate `CAREERS_DATA` with the full skill lists from Mythras p.27-32 (data below).
b) When player selects a career in Step 8, auto-populate:
   - All 7 standard skills (shown as checkboxes or auto-added)
   - Professional skills shown as a pick-3 selector (player chooses up to 3 from the 7 available)
c) Step 9 (Career Skills & Magic) then shows only the selected career skills for point distribution.

## Career Skills Data (from Mythras Core Rulebook p.27-32)

```json
[
  {
    "name": "Agent",
    "standardSkills": ["Conceal", "Deceit", "Evade", "Insight", "Perception", "Stealth"],
    "combatStyles": ["Combat Style (Concealable Weapons Style)"],
    "professionalSkills": ["Culture (any)", "Disguise", "Language (any)", "Sleight", "Streetwise", "Survival", "Track"]
  },
  {
    "name": "Alchemist",
    "standardSkills": ["Customs", "Endurance", "First Aid", "Insight", "Locale", "Perception", "Willpower"],
    "combatStyles": [],
    "professionalSkills": ["Commerce", "Craft (Alchemy)", "Healing", "Language (any)", "Literacy", "Lore (Specific Alchemical Speciality)", "Streetwise"]
  },
  {
    "name": "Beast Handler",
    "standardSkills": ["Drive", "Endurance", "First Aid", "Influence", "Locale", "Ride", "Willpower"],
    "combatStyles": [],
    "professionalSkills": ["Commerce", "Craft (Animal Husbandry)", "Healing (Specific Species)", "Lore (Specific Species)", "Survival", "Teach (Specific Species)", "Track"]
  },
  {
    "name": "Courtesan",
    "standardSkills": ["Customs", "Dance", "Deceit", "Influence", "Insight", "Perception", "Sing"],
    "combatStyles": [],
    "professionalSkills": ["Art (any)", "Courtesy", "Culture (any)", "Gambling", "Language (any)", "Musicianship", "Seduction"]
  },
  {
    "name": "Courtier",
    "standardSkills": ["Customs", "Dance", "Deceit", "Influence", "Insight", "Locale", "Perception"],
    "combatStyles": [],
    "professionalSkills": ["Art (any)", "Bureaucracy", "Courtesy", "Culture (any)", "Language (any)", "Lore (any)", "Oratory"]
  },
  {
    "name": "Crafter",
    "standardSkills": ["Brawn", "Drive", "Influence", "Insight", "Locale", "Perception", "Willpower"],
    "combatStyles": [],
    "professionalSkills": ["Art (any)", "Commerce", "Craft (Primary)", "Craft (Secondary)", "Engineering", "Mechanisms", "Streetwise"]
  },
  {
    "name": "Entertainer",
    "standardSkills": ["Athletics", "Brawn", "Dance", "Deceit", "Influence", "Insight", "Sing"],
    "combatStyles": [],
    "professionalSkills": ["Acrobatics", "Acting", "Oratory", "Musicianship", "Seduction", "Sleight", "Streetwise"]
  },
  {
    "name": "Farmer",
    "standardSkills": ["Athletics", "Brawn", "Drive", "Endurance", "Locale", "Perception", "Ride"],
    "combatStyles": [],
    "professionalSkills": ["Commerce", "Craft (any)", "Lore (Agriculture)", "Lore (Animal Husbandry)", "Navigation", "Survival", "Track"]
  },
  {
    "name": "Fisher",
    "standardSkills": ["Athletics", "Boating", "Endurance", "Locale", "Perception", "Stealth", "Swim"],
    "combatStyles": [],
    "professionalSkills": ["Commerce", "Craft (any)", "Lore (Primary Catch)", "Lore (Secondary Catch)", "Navigation", "Seamanship", "Survival"]
  },
  {
    "name": "Herder",
    "standardSkills": ["Endurance", "First Aid", "Insight", "Locale", "Perception", "Ride"],
    "combatStyles": ["Combat Style (Specific Herding or Cultural Style)"],
    "professionalSkills": ["Commerce", "Craft (Animal Husbandry)", "Healing (Specific Species)", "Navigation", "Musicianship", "Survival", "Track"]
  },
  {
    "name": "Hunter",
    "standardSkills": ["Athletics", "Endurance", "Locale", "Perception", "Ride", "Stealth"],
    "combatStyles": ["Combat Style (Specific Hunting or Cultural Style)"],
    "professionalSkills": ["Commerce", "Craft (Hunting Related)", "Lore (Regional or Specific Species)", "Mechanisms", "Navigation", "Survival", "Track"]
  },
  {
    "name": "Merchant",
    "standardSkills": ["Boating", "Drive", "Deceit", "Insight", "Influence", "Locale", "Ride"],
    "combatStyles": [],
    "professionalSkills": ["Commerce", "Courtesy", "Culture (any)", "Language (any)", "Navigation", "Seamanship", "Streetwise"]
  },
  {
    "name": "Miner",
    "standardSkills": ["Athletics", "Brawn", "Endurance", "Locale", "Perception", "Sing", "Willpower"],
    "combatStyles": [],
    "professionalSkills": ["Commerce", "Craft (Mining)", "Engineering", "Lore (Minerals)", "Mechanisms", "Navigation (Underground)", "Survival"]
  },
  {
    "name": "Mystic",
    "standardSkills": ["Athletics", "Endurance", "Evade", "Insight", "Perception", "Willpower"],
    "combatStyles": ["Combat Style (Cultural Style)"],
    "professionalSkills": ["Art (any)", "Folk Magic", "Literacy", "Lore (any)", "Meditation", "Musicianship", "Mysticism"]
  },
  {
    "name": "Official",
    "standardSkills": ["Customs", "Deceit", "Influence", "Insight", "Locale", "Perception", "Willpower"],
    "combatStyles": [],
    "professionalSkills": ["Bureaucracy", "Commerce", "Courtesy", "Language (any)", "Literacy", "Lore (any)", "Oratory"]
  },
  {
    "name": "Physician",
    "standardSkills": ["Dance", "First Aid", "Influence", "Insight", "Locale", "Sing", "Willpower"],
    "combatStyles": [],
    "professionalSkills": ["Commerce", "Craft (Specific Physiological Speciality)", "Healing", "Language (any)", "Literacy", "Lore (Specific Alchemical Speciality)", "Streetwise"]
  },
  {
    "name": "Priest",
    "standardSkills": ["Customs", "Dance", "Deceit", "Influence", "Insight", "Locale", "Willpower"],
    "combatStyles": [],
    "professionalSkills": ["Bureaucracy", "Devotion (Pantheon, Cult or God)", "Exhort", "Folk Magic", "Literacy", "Lore (any)", "Oratory"]
  },
  {
    "name": "Sailor",
    "standardSkills": ["Athletics", "Boating", "Brawn", "Endurance", "Locale", "Swim"],
    "combatStyles": ["Combat Style (Specific Shipboard or Cultural Style)"],
    "professionalSkills": ["Craft (Specific Shipboard Speciality)", "Culture (any)", "Language (any)", "Lore (any)", "Navigation", "Seamanship", "Survival"]
  },
  {
    "name": "Scholar",
    "standardSkills": ["Customs", "Influence", "Insight", "Locale", "Native Tongue", "Perception", "Willpower"],
    "combatStyles": [],
    "professionalSkills": ["Culture (any)", "Language (any)", "Literacy", "Lore (Primary)", "Lore (Secondary)", "Oratory", "Teach"]
  },
  {
    "name": "Scout",
    "standardSkills": ["Athletics", "Endurance", "First Aid", "Perception", "Stealth", "Swim"],
    "combatStyles": ["Combat Style (Specific Hunting or Cultural Style)"],
    "professionalSkills": ["Culture (any)", "Healing", "Language (any)", "Lore (any)", "Navigation", "Survival", "Track"]
  },
  {
    "name": "Shaman",
    "standardSkills": ["Customs", "Dance", "Deceit", "Influence", "Insight", "Locale", "Willpower"],
    "combatStyles": [],
    "professionalSkills": ["Binding (Cult, Totem or Tradition)", "Folk Magic", "Healing", "Lore (any)", "Oratory", "Sleight", "Trance"]
  },
  {
    "name": "Sorcerer",
    "standardSkills": ["Customs", "Deceit", "Influence", "Insight", "Locale", "Perception", "Willpower"],
    "combatStyles": [],
    "professionalSkills": ["Folk Magic", "Invocation (Cult, School or Grimoire)", "Language (any)", "Literacy", "Lore (any)", "Shaping", "Sleight"]
  },
  {
    "name": "Thief",
    "standardSkills": ["Athletics", "Deceit", "Evade", "Insight", "Perception", "Stealth"],
    "combatStyles": ["Combat Style (Concealable Weapons Style)"],
    "professionalSkills": ["Acting", "Commerce", "Disguise", "Lockpicking", "Mechanisms", "Sleight", "Streetwise"]
  },
  {
    "name": "Warrior",
    "standardSkills": ["Athletics", "Brawn", "Endurance", "Evade", "Unarmed"],
    "combatStyles": ["Combat Style (Cultural Style)", "Combat Style (Speciality Style)"],
    "professionalSkills": ["Craft (any)", "Engineering", "Gambling", "Lore (Military History)", "Lore (Strategy and Tactics)", "Oratory", "Survival"]
  }
]
```

## Also fix: Weapon AP/HP data
Many weapons have null AP/HP values because the spreadsheet parser mapped the wrong columns. The raw data has AP in column M and HP in column N of the Calculations-Weapons sheet. Re-parse from `references/spreadsheet-extract.txt` to fix. Grep for the weapons section starting at "SHEET: Calculations-Weapons" and extract columns M (AP) and N (HP) for each weapon row.

## Constraints
- Single file: all changes in `aig-character-sheet.html`
- Also update `data/careers.json` with the career skills data above
- Run tests after changes: `cd /home/node/.openclaw/devbox-env && devbox run -- uv run --with pytest pytest /tmp/aig-character-sheet/tests/test_calculations.py -v`
- Commit to branch `fix/v1-ux-issues`
- Push when done
