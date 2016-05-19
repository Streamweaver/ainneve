"""
Utility objects.
"""
from evennia.contrib import dice

# from evennia import TICKER_HANDLER as tickerhandler
# from world import archetypes, races, skills
#
#
# def sample_char(char, archetype, race, focus=None):
#     """Loads sample traits onto a character.
#
#     Args:
#         char (Character): character to load traits
#         archetype (str): name of base archetype
#         race (str): name of race to become
#         focus Optional(str): focus to apply. if None, default is race's
#             first item in foci collection
#         """
#     archetypes.apply_archetype(char, archetype, reset=True)
#     char.traits.STR.base += 1
#     char.traits.PER.base += 1
#     char.traits.INT.base += 1
#     char.traits.DEX.base += 1
#     char.traits.CHA.base += 1
#     char.traits.VIT.base += 2
#     char.traits.MAG.base += 2
#     focus = focus or races.load_race(race).foci[0]
#     races.apply_race(char, race, focus)
#     archetypes.calculate_secondary_traits(char.traits)
#     archetypes.finalize_traits(char.traits)
#     tickerhandler.add(char, 6, hook_key='at_turn_start')
#     skills.apply_skills(char)
#     skills.finalize_skills(char.skills)

def d6str(value):
    """
    Formats a value as a D6 string.  i.e 3D, 2D+2, ...
    Args:
        value (int): Value to convert.

    Returns:
        (String) of D6 notation for value.
    """
    if value < 3:
        return ""
    d = value / 3
    p = value % 3
    rslt = "{}D".format(d) if p < 1 else "{}D+{}".format(d, p)
    return rslt

def d6roll(value):
    """
    Rolls the D6 rating for value and returns the results.

    Args:
        value (int):  D6 value to roll.

    Returns:
        (int) of the result of the #D6+# roll.
    """
    if value < 3:
        return 0
    d = value / 3
    p = value % 3
    if p == 0:
        return dice.roll_dice(d, 6)
    else:
        return dice.roll_dice(d, 6, ('+', p))