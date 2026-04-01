#!/usr/bin/env python3
"""
Mythras/AiG Character Sheet Calculation Engine

All formulas extracted from AiG Auto-Calculating Sheet V1.06.
Deterministic, testable calculation functions for character attributes,
skills, and derived statistics.
"""

import math
from typing import Dict, Tuple, Optional


# ==============================================================================
# DAMAGE MODIFIER TABLE (from calculations A57:B60)
# ==============================================================================

DAMAGE_MOD_TABLE = {
    1: '-1d8', 2: '-1d6', 3: '-1d4', 4: '-1d2', 5: '0',
    6: '1d2', 7: '1d4', 8: '1d6', 9: '1d8', 10: '1d10',
    11: '1d12', 12: '1d12', 13: '2d6', 14: '2d6',
    15: '1d8+1d6', 16: '1d8+1d6', 17: '2d8', 18: '2d8',
    19: '1d10+1d8', 20: '1d10+1d8'
}


# ==============================================================================
# AGE CATEGORIES (from calculations N146:R224)
# ==============================================================================

AGE_TABLE = [
    {'min': 12, 'max': 16, 'category': 'Young', 'bonus_points': 100, 'max_per_skill': 10, 'bg_events': 0},
    {'min': 17, 'max': 27, 'category': 'Adult', 'bonus_points': 150, 'max_per_skill': 15, 'bg_events': 1},
    {'min': 28, 'max': 42, 'category': 'Middle Aged', 'bonus_points': 200, 'max_per_skill': 20, 'bg_events': 2},
    {'min': 43, 'max': 57, 'category': 'Senior', 'bonus_points': 250, 'max_per_skill': 25, 'bg_events': 3},
    {'min': 58, 'max': 999, 'category': 'Old', 'bonus_points': 300, 'max_per_skill': 30, 'bg_events': 4}
]


# ==============================================================================
# DIFFICULTY MODIFIERS (from calculations A63:B68)
# ==============================================================================

DIFFICULTY_MODS = {
    'Very Easy': 2.0,
    'Easy': 1.5,
    'Standard': 1.0,
    'Hard': 0.66,
    'Formidable': 0.5,
    'Herculean': 0.1
}


# ==============================================================================
# CORE ATTRIBUTES (from datasheet B19:D26)
# ==============================================================================

def action_points(dex: int, int_stat: int) -> int:
    """Action Points = ROUNDUP((DEX + INT) / 12)"""
    return math.ceil((dex + int_stat) / 12)


def experience_modifier(cha: int) -> int:
    """Experience Modifier = ROUNDUP(CHA / 6) - 2"""
    return math.ceil(cha / 6) - 2


def healing_rate(con: int) -> int:
    """Healing Rate = ROUNDUP(CON / 6)"""
    return math.ceil(con / 6)


def luck_points(pow: int) -> int:
    """Luck Points = ROUNDUP(POW / 6)"""
    return math.ceil(pow / 6)


def magic_points(pow: int) -> int:
    """Magic Points = POW"""
    return pow


def initiative_bonus(dex: int, int_stat: int) -> int:
    """Initiative Bonus = ROUNDUP(AVERAGE(DEX, INT))"""
    return round((dex + int_stat) / 2)


def damage_modifier(str_stat: int, siz: int) -> str:
    """Damage Modifier lookup from (STR + SIZ) / 5, ceiling"""
    combined = math.ceil((str_stat + siz) / 5)
    # Clamp to table range
    combined = max(1, min(20, combined))
    return DAMAGE_MOD_TABLE[combined]


# ==============================================================================
# HIT POINTS PER LOCATION (humanoid 7-location, from datasheet B28:C33)
# ==============================================================================

def hit_points_per_location(con: int, siz: int) -> Dict[str, int]:
    """
    Calculate HP per location for humanoid characters.
    Base = ROUNDUP((CON + SIZ) / 5)

    Returns dict with keys: head, chest, abdomen, right_arm, left_arm, right_leg, left_leg
    """
    base = math.ceil((con + siz) / 5)
    return {
        'head': base,
        'chest': base + 2,
        'abdomen': base + 1,
        'right_arm': max(base - 1, 1),
        'left_arm': max(base - 1, 1),
        'right_leg': base,
        'left_leg': base
    }


# ==============================================================================
# ENCUMBRANCE (from calculations A57:B60)
# ==============================================================================

def encumbrance_thresholds(str_stat: int) -> Dict[str, int]:
    """
    Calculate encumbrance thresholds based on STR.

    Returns dict with keys: unencumbered, burdened, overloaded, no_movement
    """
    return {
        'unencumbered': str_stat * 2,
        'burdened': str_stat * 2 + 1,
        'overloaded': str_stat * 3 + 1,
        'no_movement': str_stat * 4
    }


# ==============================================================================
# RUNE AFFINITIES (AiG p.24)
# ==============================================================================

def rune_affinity_values(pow: int) -> Tuple[int, int, int]:
    """
    Calculate base values for three rune affinities.
    Primary: POW × 2 + 30
    Secondary: POW × 2 + 20
    Tertiary: POW × 2 + 10

    Returns (primary, secondary, tertiary)
    """
    base = pow * 2
    return (base + 30, base + 20, base + 10)


def rune_skill_base(pow: int, other: int = 0) -> int:
    """
    Base for individual rune skills: POW × 2 + other
    """
    return pow * 2 + other


# ==============================================================================
# FOLK MAGIC (AiG p.24)
# ==============================================================================

def folk_magic_base(pow: int, cha: int) -> int:
    """Folk Magic skill base = POW + CHA + 30"""
    return pow + cha + 30


# ==============================================================================
# DEVOTIONAL POOL (from CULTS sheet)
# ==============================================================================

def devotional_pool(rank: str, current_pow: int) -> int:
    """
    Calculate devotional pool based on cult rank and current POW.
    Only applies to Theist cults.

    Args:
        rank: One of 'High Priest', 'Priest', 'Acolyte', 'Initiate', 'Lay Member'
        current_pow: Current POW characteristic

    Returns:
        Devotional pool size (0 for non-theist ranks)
    """
    rank_multipliers = {
        'High Priest': 1.0,
        'Priest': 0.75,
        'Acolyte': 0.5,
        'Initiate': 0.25,
        'Lay Member': 0.0
    }
    multiplier = rank_multipliers.get(rank, 0.0)
    return math.ceil(current_pow * multiplier)


# ==============================================================================
# AGE-RELATED CALCULATIONS
# ==============================================================================

def get_age_category(age: int) -> Optional[Dict]:
    """
    Get age category data for a given age.

    Returns dict with: category, bonus_points, max_per_skill, bg_events
    Or None if age is out of range.
    """
    for category in AGE_TABLE:
        if category['min'] <= age <= category['max']:
            return category
    return None


# ==============================================================================
# SKILL CALCULATIONS
# ==============================================================================

def skill_base_value(stat1: int, stat2: int, starting_bonus: int = 0) -> int:
    """
    Calculate base value for a skill.
    Base = Stat1 + Stat2 + starting_bonus

    Examples:
    - Athletics: STR + DEX
    - Customs: INT + INT + 40
    - Endurance: CON + CON
    """
    return stat1 + stat2 + starting_bonus


def skill_total(base: int, culture: int = 0, career: int = 0, bonus: int = 0, other: int = 0) -> int:
    """
    Calculate total skill value.
    Total = base + culture + career + bonus + other
    """
    return base + culture + career + bonus + other


def apply_difficulty_modifier(skill_total: int, difficulty: str) -> int:
    """
    Apply difficulty modifier to a skill total.
    Applied skill = ROUNDUP(skill_total × modifier)

    Args:
        skill_total: Base skill percentage
        difficulty: One of 'Very Easy', 'Easy', 'Standard', 'Hard', 'Formidable', 'Herculean'

    Returns:
        Modified skill percentage
    """
    modifier = DIFFICULTY_MODS.get(difficulty, 1.0)
    return math.ceil(skill_total * modifier)


# ==============================================================================
# HEIGHT AND WEIGHT (from calculations, based on SIZ + frame)
# ==============================================================================

def height_weight_by_siz(siz: int, frame: str = 'Medium') -> Tuple[int, int]:
    """
    Calculate height (cm) and weight (kg) based on SIZ and frame.

    Args:
        siz: SIZ characteristic (1-21+)
        frame: 'Lithe', 'Medium', or 'Heavy'

    Returns:
        (height_cm, weight_kg)

    Note: This is a simplified approximation. The actual spreadsheet
    uses complex lookup tables.
    """
    # Base height from SIZ (rough approximation)
    base_height = 150 + (siz - 10) * 5  # cm

    # Base weight from SIZ
    base_weight = 50 + (siz - 10) * 5  # kg

    # Frame modifiers
    frame_mods = {
        'Lithe': (0.95, 0.85),
        'Medium': (1.0, 1.0),
        'Heavy': (1.05, 1.2)
    }
    height_mod, weight_mod = frame_mods.get(frame, (1.0, 1.0))

    return (int(base_height * height_mod), int(base_weight * weight_mod))


# ==============================================================================
# COMPLETE CHARACTER ATTRIBUTES CALCULATION
# ==============================================================================

def calculate_all_attributes(characteristics: Dict[str, int]) -> Dict[str, any]:
    """
    Calculate all derived attributes from characteristics.

    Args:
        characteristics: Dict with keys STR, CON, SIZ, DEX, INT, POW, CHA

    Returns:
        Dict with all derived attributes
    """
    STR = characteristics['STR']
    CON = characteristics['CON']
    SIZ = characteristics['SIZ']
    DEX = characteristics['DEX']
    INT = characteristics['INT']
    POW = characteristics['POW']
    CHA = characteristics['CHA']

    return {
        'action_points': action_points(DEX, INT),
        'experience_modifier': experience_modifier(CHA),
        'healing_rate': healing_rate(CON),
        'luck_points': luck_points(POW),
        'magic_points': magic_points(POW),
        'initiative_bonus': initiative_bonus(DEX, INT),
        'damage_modifier': damage_modifier(STR, SIZ),
        'hit_points': hit_points_per_location(CON, SIZ),
        'encumbrance': encumbrance_thresholds(STR),
        'rune_affinities': rune_affinity_values(POW),
        'folk_magic_base': folk_magic_base(POW, CHA)
    }


# ==============================================================================
# MOVEMENT RATE (from Mythras p.12, based on race and DEX)
# ==============================================================================

def movement_rate(race: str = 'Human') -> int:
    """
    Base movement rate in meters.
    Human default: 6m per combat round.
    """
    # For AiG, we only support humans
    return 6


# ==============================================================================
# MAIN FUNCTION FOR TESTING
# ==============================================================================

if __name__ == '__main__':
    # Test with sample character from spreadsheet
    # STR=11, CON=13, SIZ=10, DEX=16, INT=14, POW=7, CHA=9

    test_char = {
        'STR': 11,
        'CON': 13,
        'SIZ': 10,
        'DEX': 16,
        'INT': 14,
        'POW': 7,
        'CHA': 9
    }

    print("Test Character Attributes:")
    print(f"Characteristics: {test_char}")
    print()

    attributes = calculate_all_attributes(test_char)

    print("Derived Attributes:")
    for key, value in attributes.items():
        print(f"  {key}: {value}")

    print()
    print("Age Category Tests:")
    for test_age in [15, 20, 35, 50, 65]:
        cat = get_age_category(test_age)
        print(f"  Age {test_age}: {cat['category']} - {cat['bonus_points']} points, max {cat['max_per_skill']} per skill")

    print()
    print("Difficulty Modifier Tests:")
    base_skill = 50
    for diff in ['Very Easy', 'Easy', 'Standard', 'Hard', 'Formidable', 'Herculean']:
        modified = apply_difficulty_modifier(base_skill, diff)
        print(f"  {base_skill}% at {diff}: {modified}%")
