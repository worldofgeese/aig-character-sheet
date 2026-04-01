# Fix Brief: Pocketfold Print + AiG Acronym Expansion

## Branch
Work on branch `fix/v3-pocketfold-newplayer`. Do NOT merge to main.

## Issues (2 features)

### Feature 1: Replace "AiG" with "Adventures in Glorantha"

There are 13 occurrences of "AiG" in page references like `(AiG p.24)`. Replace ALL of them with the full name "Adventures in Glorantha". This is a new-player-friendly character sheet — players may not know what "AiG" stands for.

Pattern: `(AiG p.XX)` → `(Adventures in Glorantha p.XX)`

Also check for any `(AiG p.XX, ...)` patterns and handle those too, e.g.:
- `(AiG p.23, Mythras p.9-11)` → `(Adventures in Glorantha p.23, Mythras p.9-11)`
- `(AiG p.23, p.25-41)` → `(Adventures in Glorantha p.23, p.25-41)`

### Feature 2: Pocketfold Print Layout

Add a "Print Pocketfold" button (next to the existing "Print (A4)" button). This creates an 8-panel pocket booklet from a single A4 sheet.

#### Pocketfold Layout (A4 Landscape)

The sheet is A4 landscape. It has a 4×2 grid of panels. The TOP row panels are rotated 180°. After printing, the player cuts and folds to make an 8-page mini-booklet.

```
TOP ROW (all rotated 180°):
+----------+----------+----------+----------+
| Panel 7  | Panel 6  | Panel 5  | Panel 4  |
| (upside  | (upside  | (upside  | (upside  |
|  down)   |  down)   |  down)   |  down)   |
+----------+----------+----------+----------+
| Panel 3  | Panel 8  | Panel 1  | Panel 2  |
| (normal) | (normal) | (normal) | (normal) |
+----------+----------+----------+----------+
BOTTOM ROW (all normal orientation)
```

#### Panel Content Assignment

| Panel | Content |
|-------|---------|
| 1 (Cover) | Character name, culture, career, age. Title "Adventures in Glorantha" |
| 2 | Characteristics (STR/CON/SIZ/DEX/INT/POW/CHA) + Attributes (AP, DM, HP, etc.) |
| 3 | Hit Locations table with HP/AP per location |
| 4 | Key Skills (only skills with points allocated, not all 100+ skills) |
| 5 | More Skills (overflow from panel 4) |
| 6 | Combat: weapons, combat styles, special effects summary |
| 7 | Magic: rune affinities, folk magic spells, devotion pool |
| 8 (Back cover) | Equipment list, money, notes, fold instructions link |

#### How to Print Button

Add a button: `Print Pocketfold 📖`
- Only available in Play Mode (like the A4 print button)
- When clicked, generates a pocketfold view and triggers print
- The pocketfold view is a hidden div that becomes visible only during print
- After printing, the normal view is restored

#### Implementation Approach

1. Add a hidden `#pocketfold-view` div after `#play-mode`
2. When "Print Pocketfold" is clicked:
   - Populate `#pocketfold-view` with character data in the 8-panel layout
   - Hide `#play-mode`, show `#pocketfold-view`
   - Use `@media print` CSS specific to pocketfold:
     - `@page { size: A4 landscape; margin: 0; }`
     - Grid: `display: grid; grid-template-columns: repeat(4, 1fr); grid-template-rows: repeat(2, 1fr);`
     - Top row panels: `transform: rotate(180deg);`
     - Each panel: `width: 25%; height: 50%;` of the page
     - Borders between panels (dashed, for cutting guide)
   - Call `window.print()`
   - After print dialog closes, restore normal view

3. Add fold instructions on Panel 8:
   ```
   HOW TO FOLD:
   1. Cut along the horizontal center line
   2. Fold the top strip behind the bottom strip
   3. Fold left-to-right accordion-style
   
   Video tutorial: [search "pocketmod fold" on YouTube]
   Or visit: pocketmod.com/howto
   ```

#### CSS for Pocketfold

```css
#pocketfold-view {
  display: none;
}

#pocketfold-view.printing {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  grid-template-rows: repeat(2, 1fr);
  width: 297mm;
  height: 210mm;
  font-size: 7pt;
  line-height: 1.2;
}

#pocketfold-view .panel {
  border: 0.5pt dashed #999;
  padding: 3mm;
  overflow: hidden;
  box-sizing: border-box;
}

#pocketfold-view .panel.flipped {
  transform: rotate(180deg);
}

@media print {
  #pocketfold-view.printing {
    display: grid !important;
  }
  #pocketfold-view.printing ~ * {
    display: none !important;
  }
}
```

#### Key Constraints

- Font size must be 7-8pt to fit content in panels
- Only show skills that have points allocated (base + culture + career + bonus > base)
- Skills should be compact: `Skill Name ........ XX%` format
- Hit locations as a tiny table
- Equipment as a compact list
- Panel 1 (cover) should look nice — character name large, culture/career underneath
- All text must be readable when printed at A4 landscape scale (each panel is ~74mm × 105mm)
- Use monospace or condensed font for skill lists to maximize density

## Testing

1. Run `python3 -m unittest tests.test_calculations -v` — must still pass
2. Verify zero occurrences of standalone "AiG" remain (should all be "Adventures in Glorantha")
3. Visual check: the pocketfold panels should be roughly the right size
4. Commit with descriptive message
5. Push to branch, do NOT merge
