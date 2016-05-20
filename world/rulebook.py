"""
The Ainneve rulebook.

This module is an implementation of a simplified subset of the Open
Adventure rulebook. It contains a number of utility functions for
enforcing various game rules. See individual docstrings for more info.

Roll / Check Functions

    - `d6roll(value)`
    - `skill_check(ch, skill, target=5)`
    - `skill_result(ch, skill)`

"""

from evennia.contrib import dice

class DiceRollError(Exception):
    """Default error class in die rolls/skill checks.

    Args:
        msg (str): a descriptive error message
    """
    def __init__(self, msg):
        self.msg = msg

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

def skill_result(ch, skill):
    """

    Args:
         ch (Character): Chracter object
         skill (Trait):  String of skill to check.
    """

    value = ch.traits[skill.trait].acutal + skill.actual
    return d6roll(value)

def skill_check(ch, skill, target=5):
    """A basic Open Adventure Skill check.

    This is used for skill checks, trait checks, save rolls, etc.

    Args:
        skill (Trait): the value of the skill to check
        target (int): the target number for the check to succeed

    Returns:
        (bool): indicates whether the check passed or failed
    """
    return skill + std_roll() >= target
