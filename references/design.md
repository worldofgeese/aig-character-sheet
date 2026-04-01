# AiG Character Sheet — Project Plan

## Source Material Hierarchy
1. **Adventures in Glorantha** (AiG, GenCon 2015 preview) — primary for Glorantha-specific content
2. **Mythras Core Rulebook** (3rd printing, 2018) — fallback for core mechanics, cults, magic systems
3. **AiG Auto-Calculating Sheet V1.06** (Excel) — canonical backend, every formula reproduced exactly
4. **CultOnePagers2019** (Google Drive, Notes From Pavis) — upstream cult database
   - URL: https://drive.google.com/drive/folders/1CKNxkpoL4sWfzdbkglQyiYvCBXlmyFIj
   - 20 pantheon folders (Storm, Darkness, Lunar, Yelm, etc.)
   - AiG-specific versions in "CultsAIG" folder (updated Feb 2025)

## Deliverables

### Phase 0: Hyperclay Skill (reusable foundation)
Extract generic Hyperclay patterns from `dnd-2014-character-creator` into a standalone skill.
- `skills/hyperclay/SKILL.md` — conventions, modules, save semantics, responsive patterns
- `skills/hyperclay/references/hyperclay-patterns.md` — lifted from D&D skill, generalized
- `skills/hyperclay/assets/` — blank skeleton template if useful
- Following Anthropic skill-creator structure

### Phase 1: Calculation Engine
Port all spreadsheet formulas to a Python calculation script.
- `scripts/mythras_calculations.py` — deterministic, testable
- All 7 characteristics → all derived attributes
- 147 skill base values (stat1 + stat2 + starting_bonus)
- Damage modifier table (21 rows)
- HP per location (humanoid 7-location)
- Encumbrance thresholds
- Age → bonus points / limits / background events
- Devotional pool formula
- Height/weight by SIZ + frame
- Difficulty modifier multipliers

### Phase 2: Reference Data
Extract and structure all lookup tables as JSON or JS constants.
- 360 weapons (from Calculations-Weapons)
- 147 skills with stat pairs (from Calculations-Skills)
- 33 runes with metadata (from Runes sheet)
- Equipment list with ENC (from calculations)
- Armour table (from calculations)
- **Human-only** characteristic dice (3d6 / 2d6+6) — no non-human races
- Human 7-location hit point table only (Head/Chest/Abdomen/Arms/Legs)
- Culture definitions (from AiG p.25-41)
- Career list (from calculations + Mythras p.27-32)
- Combat style traits (from Calculations-CombatStyleTraits)
- Special effects (from Special Effects Summary)
- Cult rank hierarchies (from calculations)

### Design Decision: Characteristics
- **Both point-buy and dice rolling** supported
- Point-buy default: 75 points, stats range 3-18
- Dice roller: 3d6 for STR/CON/DEX/POW/CHA, 2d6+6 for SIZ/INT
- Toggle between modes at top of Step 2
- Race: **Human only** (Glorantha-appropriate scope)

### Phase 3: Step-Driven Wizard
12-step character creation wizard matching AiG's order:
1. **Concept** — free text, guidance from AiG p.23
2. **Characteristics** — point-buy (75 points) or dice roller, race selection → (AiG p.23, Mythras p.9)
3. **Attributes** — auto-calculated, displayed with explanations → (Mythras p.9-12)
4. **Culture & Homeland** — dropdown, 8 AiG cultures → (AiG p.24-41)
5. **Cultural Skills & Magic** — 100 culture points, rune affinities, folk magic → (AiG p.24)
6. **Passions** — culture-specific starters + custom → (AiG p.24, Mythras p.23-27)
7. **Background Details** — optional community/family/background events → (Mythras p.18-22)
8. **Career** — culture-filtered career list → (AiG p.24, Mythras p.27-32)
9. **Career Skills & Magic** — 100 career points + 2 folk magic spells → (AiG p.24)
10. **Age & Bonus Points** — age-dependent points/limits → (AiG p.24-25, Mythras p.32-33)
11. **Equipment & Money** — culture-based starting money, equipment picker → (AiG p.25)
12. **Review & Play** — final summary, transition to play mode

Each step shows:
- Step number and title
- Brief explanation (new-player friendly)
- Page reference: "(AiG p.XX, Mythras p.XX)"
- Input fields
- Running point budget tracker (culture/career/bonus points remaining)
- **Hard enforcement**: cannot proceed if overspent, per-skill caps enforced by age category

### Design Decisions Log
- **Q6**: Both point-buy (default, 75pts) and dice rolling supported
- **Q7**: Human only — no non-human races
- **Q8**: Auto-fill cultural skills/combat styles/folk magic/passions on culture selection
- **Q9**: Difficulty modifier dropdown in play mode (multiplies displayed skill %)
- **Q10**: Hard enforcement on point budgets and per-skill caps — no overspending
- **Q11**: Special effects summary (41 effects) embedded as collapsible reference panel in play mode
- **Q12**: Full 360-weapon searchable database with autocomplete, auto-fills all stats, editable after
- **Q13**: Print support — A4 portrait one-page (max utility density) + Pocketfold option
  - A4 portrait: everything on one page, built for maximum information density
  - Pocketfold: 8-panel pocket booklet from single A4 sheet (cut + fold)
  - Layout logic from https://github.com/Laur401/pocketverter
  - Pocketfold panel order: [7↕,6↕,5↕,4↕ / 3,8,1,2] (↕=reversed)
  - Panel content: 1=Cover/Identity, 2=Characteristics+Attributes, 3=Skills, 
    4=Combat/Weapons, 5=Magic/Spells, 6=Passions/Runes, 7=Equipment, 8=Notes
  - Both generated from live DOM values via JS "Print" button

### Phase 4: Play Mode Sheet
After wizard completion, single-page character sheet with sections:
- Identity header (name, culture, homeland, race, career, social class)
- Characteristics + Attributes sidebar
- Skills (standard + professional + magic + combat styles + languages)
- Passions
- Hit locations with HP tracking
- Combat panel (weapons, armour, special effects reference)
- Rune affinities
- Cult information (up to 12 slots)
- Spells (folk magic, rune magic, sorcery, spirit magic)
- Equipment + encumbrance tracker
- Notes / backstory

### Phase 5: Cult Integration
- **~20 common Dragon Pass/Prax cults embedded as JSON** — searchable selector
  - Orlanth, Ernalda, Humakt, Yelmalio, Storm Bull, Chalana Arroy, Issaries, 
    Lhankor Mhy, Seven Mothers, Waha, Eiritha, Daka Fal, Babeester Gor,
    Maran Gor, Argan Argar, Zorak Zoran, Eurmal, Uleria, Lanbril, Kyger Litor
  - Each with: type, runes, rank progression, cult skills, folk magic, miracles by rank, gifts, geasa
- **Free-text fallback for all other cults** — players reference the 200+ CultOnePagers2019 PDFs
  - Link to Google Drive: https://drive.google.com/drive/folders/1CKNxkpoL4sWfzdbkglQyiYvCBXlmyFIj
  - Blank cult template with all fields (name, type, rank, benefits, restrictions, gifts, geasa, devotional pool)
- Cult type determines rank hierarchy (Theist/Animist/Sorcery/Mystical/Brotherhood)
- Devotional pool auto-calculated from rank + POW
- Up to 12 cult slots (matching spreadsheet)

### Phase 6: Verification
- Build 2-3 sample characters through both spreadsheet and HTML sheet
- Compare every derived value for exact match
- Test on mobile (responsive breakpoints)
- Test Hyperclay save/load cycle

- **Q14**: Forgejo repo at `kypris/aig-character-sheet` — versioned, testable, shareable
- **Q15**: Building now — Phase 0 → 1 → 2 → 3, ship vertical slice first

## Repository
- **Remote**: `ssh://forgejo@paphos.hound-celsius.ts.net/kypris/aig-character-sheet.git`
- **Stack**: Single Hyperclay HTML file + Python calculation engine (tests) + JSON reference data
- **First deliverable**: 12-step wizard + play mode, all formulas, 8 AiG cultures, no cult database
- **Second deliverable**: 20 embedded cults, pocketfold print, special effects panel
