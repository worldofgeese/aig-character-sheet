#!/usr/bin/env python3
"""
Parse the spreadsheet extract and create JSON files for:
1. Skills
2. Weapons
3. Special Effects
4. Combat Style Traits
5. Runes
6. Equipment
"""

import json
import re
from pathlib import Path

def parse_spreadsheet(filepath):
    """Parse the spreadsheet extract file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    sheets = {}
    current_sheet = None
    current_data = {}

    for line in lines:
        line = line.rstrip('\n')

        # Check for sheet marker
        if line.startswith('SHEET: '):
            if current_sheet and current_data:
                sheets[current_sheet] = current_data
            current_sheet = line.replace('SHEET: ', '')
            current_data = {}
            continue

        # Parse cell data
        if line.startswith('  ') and ':' in line and current_sheet:
            match = re.match(r'\s+([A-Z]+\d+):\s*(.*)', line)
            if match:
                cell_ref = match.group(1)
                value = match.group(2)

                # Skip formulas
                if value.startswith('FORMULA:'):
                    continue

                # Clean value
                value = value.strip("'\"")
                if value:
                    current_data[cell_ref] = value

    # Save last sheet
    if current_sheet and current_data:
        sheets[current_sheet] = current_data

    return sheets

def extract_skills(sheets):
    """Extract skills from Calculations-Skills sheet."""
    sheet = sheets.get('Calculations-Skills', {})
    skills = []

    # Parse table structure (columns A, B, C, D)
    row = 1
    while f'A{row}' in sheet:
        name = sheet.get(f'A{row}', '').strip()
        stat1 = sheet.get(f'B{row}', '').strip()
        stat2 = sheet.get(f'C{row}', '').strip()

        # Try to get starting bonus
        bonus_str = sheet.get(f'D{row}', '0').strip()
        try:
            bonus = int(bonus_str) if bonus_str and bonus_str.isdigit() else 0
        except:
            bonus = 0

        if name and stat1 and stat2:
            skill = {
                'name': name,
                'base_stats': [stat1, stat2],
                'starting_bonus': bonus
            }
            skills.append(skill)

        row += 1

    return skills

def extract_runes(sheets):
    """Extract runes from Runes sheet."""
    sheet = sheets.get('Runes', {})
    runes = []

    # Parse table structure (row 1 is headers, data starts at row 2)
    row = 2
    while f'A{row}' in sheet:
        rune_full = sheet.get(f'A{row}', '').strip()
        short_name = sheet.get(f'B{row}', '').strip()
        rune = sheet.get(f'C{row}', '').strip()
        meaning = sheet.get(f'D{row}', '').strip()
        traits = sheet.get(f'E{row}', '').strip()
        metal = sheet.get(f'F{row}', '').strip()
        instrument = sheet.get(f'G{row}', '').strip()
        weapon_tool = sheet.get(f'H{row}', '').strip()
        tool = sheet.get(f'I{row}', '').strip()
        weapon = sheet.get(f'J{row}', '').strip()
        action = sheet.get(f'K{row}', '').strip()
        color = sheet.get(f'L{row}', '').strip()
        direction = sheet.get(f'M{row}', '').strip()
        emotion = sheet.get(f'N{row}', '').strip()
        fauna_flora_flesh = sheet.get(f'O{row}', '').strip()
        fauna = sheet.get(f'P{row}', '').strip()
        flesh = sheet.get(f'Q{row}', '').strip()
        flora = sheet.get(f'R{row}', '').strip()
        opposite = sheet.get(f'S{row}', '').strip()
        organ = sheet.get(f'T{row}', '').strip()
        rune_type = sheet.get(f'W{row}', '').strip()
        sense = sheet.get(f'X{row}', '').strip()
        action_direction = sheet.get(f'Y{row}', '').strip()
        stone = sheet.get(f'Z{row}', '').strip()

        if rune_full:
            rune_obj = {
                'name': rune_full,
                'short_name': short_name,
                'rune': rune,
                'meaning': meaning,
                'personality_traits': traits,
                'rune_type': rune_type
            }

            # Add optional fields if they exist
            if metal: rune_obj['metal'] = metal
            if instrument: rune_obj['instrument'] = instrument
            if weapon_tool: rune_obj['weapon_and_tool'] = weapon_tool
            if tool: rune_obj['tool'] = tool
            if weapon: rune_obj['weapon'] = weapon
            if action: rune_obj['action'] = action
            if color: rune_obj['color'] = color
            if direction: rune_obj['direction'] = direction
            if emotion: rune_obj['emotion'] = emotion
            if fauna_flora_flesh: rune_obj['fauna_flora_flesh'] = fauna_flora_flesh
            if fauna: rune_obj['fauna'] = fauna
            if flesh: rune_obj['flesh'] = flesh
            if flora: rune_obj['flora'] = flora
            if opposite: rune_obj['opposite_rune'] = opposite
            if organ: rune_obj['organ'] = organ
            if sense: rune_obj['sense'] = sense
            if action_direction: rune_obj['action_direction'] = action_direction
            if stone: rune_obj['stone'] = stone

            runes.append(rune_obj)

        row += 1

    return runes

def extract_special_effects(sheets):
    """Extract special effects from Special Effects Summary sheet."""
    sheet = sheets.get('Special Effects Summary', {})
    effects = []

    # Parse table structure (row 3 onwards)
    row = 3
    while f'A{row}' in sheet:
        name = sheet.get(f'A{row}', '').strip()
        offensive = 'X' in sheet.get(f'B{row}', '')
        defensive = 'X' in sheet.get(f'C{row}', '')
        weapon_type = sheet.get(f'D{row}', '').strip()
        specific_roll = sheet.get(f'E{row}', '').strip()
        stackable = 'X' in sheet.get(f'F{row}', '')

        if name:
            effect = {
                'name': name,
                'offensive': offensive,
                'defensive': defensive,
                'stackable': stackable
            }

            if weapon_type:
                effect['specific_weapon_type'] = weapon_type
            if specific_roll:
                effect['specific_roll'] = specific_roll

            effects.append(effect)

        row += 1

        # Stop at reasonable point
        if row > 100:
            break

    return effects

def extract_combat_style_traits(sheets):
    """Extract combat style traits from Calculations-CombatStyleTraits sheet."""
    sheet = sheets.get('Calculations-CombatStyleTraits', {})
    traits = []

    # Parse table structure (row 2 onwards, row 1 is headers)
    row = 2
    while f'A{row}' in sheet:
        name = sheet.get(f'A{row}', '').strip()
        explanation = sheet.get(f'B{row}', '').strip()

        if name:
            trait = {
                'name': name,
                'explanation': explanation
            }
            traits.append(trait)

        row += 1

    return traits

def extract_weapons(sheets):
    """Extract weapons from Calculations-Weapons sheet."""
    sheet = sheets.get('Calculations-Weapons', {})
    weapons = []

    # Parse table structure (row 2 onwards, row 1 is headers)
    row = 2
    while f'B{row}' in sheet:  # Column B has the weapon name
        name = sheet.get(f'B{row}', '').strip()
        weapon_type = sheet.get(f'C{row}', '').strip()
        handedness = sheet.get(f'D{row}', '').strip()
        damage = sheet.get(f'E{row}', '').strip()
        size = sheet.get(f'F{row}', '').strip()
        reach = sheet.get(f'G{row}', '').strip()
        damage_mod = sheet.get(f'H{row}', '').strip()
        offensive_effects = sheet.get(f'K{row}', '').strip()
        defensive_effects = sheet.get(f'L{row}', '').strip()
        ap = sheet.get(f'M{row}', '').strip()
        hp = sheet.get(f'N{row}', '').strip()
        enc = sheet.get(f'O{row}', '').strip()
        max_range = sheet.get(f'P{row}', '').strip()
        traits = sheet.get(f'Q{row}', '').strip()
        comment = sheet.get(f'R{row}', '').strip()
        description = sheet.get(f'W{row}', '').strip()

        if name and name != '?':
            weapon = {
                'name': name,
                'weapon_type': weapon_type,
                'handedness': handedness
            }

            # Add optional fields
            if damage: weapon['damage'] = damage
            if size: weapon['size'] = size
            if reach: weapon['reach'] = reach
            if damage_mod: weapon['damage_modifier'] = damage_mod
            if offensive_effects: weapon['offensive_special_effects'] = offensive_effects
            if defensive_effects: weapon['defensive_special_effects'] = defensive_effects
            if ap:
                try:
                    weapon['armour_points'] = int(ap)
                except:
                    weapon['armour_points'] = ap
            if hp:
                try:
                    weapon['hit_points'] = int(hp)
                except:
                    weapon['hit_points'] = hp
            if enc:
                try:
                    weapon['encumbrance'] = int(enc)
                except:
                    weapon['encumbrance'] = enc
            if max_range: weapon['max_range'] = max_range
            if traits: weapon['traits'] = traits
            if comment: weapon['comment'] = comment
            if description: weapon['description'] = description

            weapons.append(weapon)

        row += 1

    return weapons

def extract_equipment(sheets):
    """Extract equipment from calculations sheet."""
    sheet = sheets.get('calculations', {})
    equipment = []

    # Equipment data starts at row 8, columns G (item name) and H (ENC)
    # Continue until we run out of items
    row = 8
    while f'G{row}' in sheet:
        name = sheet.get(f'G{row}', '').strip()
        enc_value = sheet.get(f'H{row}', '').strip()

        if name:
            item = {
                'name': name
            }

            # Parse ENC value
            if enc_value and enc_value != '-':
                try:
                    item['encumbrance'] = int(enc_value)
                except:
                    item['encumbrance'] = enc_value

            equipment.append(item)

        row += 1

        # Stop at reasonable point (when we hit empty rows or other data)
        if row > 100:
            break

    return equipment

def main():
    # Parse spreadsheet
    print("Parsing spreadsheet...")
    sheets = parse_spreadsheet('/tmp/aig-character-sheet/references/spreadsheet-extract.txt')
    print(f"Found {len(sheets)} sheets")

    # Create data directory
    data_dir = Path('/tmp/aig-character-sheet/data')
    data_dir.mkdir(exist_ok=True)

    # Extract and save skills
    print("Extracting skills...")
    skills = extract_skills(sheets)
    print(f"Found {len(skills)} skills")
    with open(data_dir / 'skills.json', 'w') as f:
        json.dump(skills, f, indent=2)

    # Extract and save runes
    print("Extracting runes...")
    runes = extract_runes(sheets)
    print(f"Found {len(runes)} runes")
    with open(data_dir / 'runes.json', 'w') as f:
        json.dump(runes, f, indent=2)

    # Extract and save special effects
    print("Extracting special effects...")
    effects = extract_special_effects(sheets)
    print(f"Found {len(effects)} special effects")
    with open(data_dir / 'special-effects.json', 'w') as f:
        json.dump(effects, f, indent=2)

    # Extract and save combat style traits
    print("Extracting combat style traits...")
    traits = extract_combat_style_traits(sheets)
    print(f"Found {len(traits)} combat style traits")
    with open(data_dir / 'combat-style-traits.json', 'w') as f:
        json.dump(traits, f, indent=2)

    # Extract and save weapons
    print("Extracting weapons...")
    weapons = extract_weapons(sheets)
    print(f"Found {len(weapons)} weapons")
    with open(data_dir / 'weapons.json', 'w') as f:
        json.dump(weapons, f, indent=2)

    # Extract and save equipment
    print("Extracting equipment...")
    equipment = extract_equipment(sheets)
    print(f"Found {len(equipment)} equipment items")
    with open(data_dir / 'equipment.json', 'w') as f:
        json.dump(equipment, f, indent=2)

    print("\nDone! JSON files created in data/ directory")

if __name__ == '__main__':
    main()
