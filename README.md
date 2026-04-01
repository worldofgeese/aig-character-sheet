# Adventures in Glorantha Character Sheet

A complete, single-file HTML character sheet for Adventures in Glorantha (Mythras engine) with a 12-step creation wizard and interactive play mode.

## Quick Start

1. Open `aig-character-sheet.html` in any modern web browser
2. Follow the 12-step wizard to create your character
3. Click "Complete" to enter Play Mode
4. Use the sheet during gameplay with live calculations
5. Save your character with Ctrl+S

## Features

### Character Creation Wizard (12 Steps)
- **Step 1:** Character concept
- **Step 2:** Characteristics (point-buy or dice rolling)
- **Step 3:** Auto-calculated attributes
- **Step 4:** Culture selection (8 Gloranthan cultures)
- **Step 5:** Cultural skills (100 points) + 3 rune affinities + 3 folk magic spells
- **Step 6:** Passions
- **Step 7:** Background details
- **Step 8:** Career selection (24 careers)
- **Step 9:** Career skills (100 points) + 2 more folk magic spells
- **Step 10:** Age-dependent bonus points
- **Step 11:** Equipment and starting money
- **Step 12:** Review and transition to play mode

### Play Mode
- Live character sheet with all stats
- Difficulty modifier dropdown
- Editable skills table with auto-calculation
- Hit location tracker
- Combat panel with weapons
- Magic spells display
- Equipment and encumbrance
- Special effects reference (44 effects)

### Technical Features
- **Single self-contained file** - No internet required
- **No frameworks** - Pure vanilla JavaScript
- **Auto-save** - Character data persists in browser
- **Import/Export** - Save/load characters as JSON
- **Print support** - A4 portrait optimized
- **Responsive** - Works on desktop, tablet, and mobile
- **Keyboard shortcuts** - Ctrl+S to save

### Embedded Data
- 147 skills with base statistics
- 360 weapons with full stats
- All equipment with encumbrance values
- 33 Gloranthan runes
- 8 cultures with complete details
- 24 careers
- 44 combat special effects
- Combat style traits

### Calculation Engine
All formulas from the official AiG spreadsheet:
- Action Points, Initiative, Damage Modifier
- Hit Points per location (7-location humanoid)
- Encumbrance thresholds
- Rune affinities
- Folk Magic base
- Skill base values from characteristics
- Difficulty modifiers (×0.1 to ×2.0)

## File Structure

```
aig-character-sheet/
├── aig-character-sheet.html    (225 KB - THE DELIVERABLE)
├── data/                        (source data, for reference)
│   ├── skills.json
│   ├── weapons.json
│   ├── equipment.json
│   ├── runes.json
│   ├── cultures.json
│   ├── careers.json
│   ├── special-effects.json
│   └── combat-style-traits.json
├── scripts/
│   └── mythras_calculations.py  (formula reference)
├── BUILD_SUMMARY.md             (detailed build report)
└── README.md                    (this file)
```

## Usage Guide

### Creating a Character

1. **Wizard Mode:** Follow steps 1-12 to build your character
2. **Point Budgets:** Hard enforcement prevents overspending
3. **Auto-calculation:** All derived stats update automatically
4. **Page References:** Each step shows relevant AiG/Mythras pages
5. **Validation:** Can't proceed until step requirements are met

### Playing with the Sheet

1. **Switch to Play Mode:** Click "Complete" or use the mode toggle
2. **Difficulty Modifier:** Set once, applies to all skill rolls
3. **Edit Values:** Click any field to update (auto-saves)
4. **Track Resources:** Hit points, magic points, luck points
5. **Combat:** Weapons list with all stats readily visible
6. **Special Effects:** Collapsible reference panel

### Saving and Loading

- **Auto-save:** Every change saves to browser localStorage
- **Export:** Click "Save" or press Ctrl+S to download JSON
- **Import:** Click "Load" to restore from JSON file
- **Print:** Click "Print" for A4 portrait output

## Browser Compatibility

- ✅ Chrome/Edge 90+
- ✅ Firefox 88+
- ✅ Safari 14+
- ✅ Mobile browsers (responsive layout)

## Design Philosophy

### Hyperclay Principles
- Dense, functional design (maximum information density)
- No decorative elements, gradients, or shadows
- System fonts only (no external dependencies)
- Single-file distribution
- Offline-capable
- Works without internet

### User Experience
- Step-by-step guidance for new players
- Hard budget enforcement prevents errors
- Auto-calculation reduces mental load
- Page references help learning
- Toast notifications for feedback
- Keyboard shortcuts for power users

## Technical Notes

### No External Dependencies
- No CDN links
- No external fonts
- No frameworks or libraries
- All data embedded as JavaScript constants
- Works completely offline

### Performance
- 225 KB total file size
- Loads instantly (no network requests)
- Smooth interactions (vanilla JS)
- LocalStorage for persistence
- No build step required

### Maintenance
- Single file makes distribution easy
- All formulas documented and ported from Python
- Data files in `/data/` for updates
- Modular JavaScript structure

## Credits

Based on:
- Adventures in Glorantha (Chaosium/Design Mechanism)
- Mythras Core Rules (Design Mechanism)
- AiG Auto-Calculating Sheet V1.06

Built with:
- Pure HTML5, CSS3, JavaScript (ES6)
- No frameworks or external dependencies
- Hyperclay design conventions

## License

This is a fan-created tool for personal use with Adventures in Glorantha.
All game content belongs to Chaosium and The Design Mechanism.

## Support

For issues or suggestions:
- Check BUILD_SUMMARY.md for implementation details
- Verify browser compatibility
- Ensure JavaScript is enabled
- Clear localStorage if experiencing issues

## Future Enhancements (Not in v1)

- Non-human races
- Cult database
- Pocketfold print layout
- Background events tables
- Advanced magic systems (sorcery, spirit magic)
- Combat simulator
- Experience tracking
