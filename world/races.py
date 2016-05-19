"""
Races module.

This module contains data and functions relating to Races and Focuses. Its
public module functions are to be used primarily during the character
creation process.

Classes:

    `Race`: base class for all races
    `Human`: human race class

Module Functions:

    - `load_race(str)`:

        loads an instance of the named Race class

    - `load_focus(str)`:

        loads an instance of the named Focus class

    - `apply_race(char, race)`:

        have a character "become" a member of the specified race.
"""

from evennia.utils import fill

class RaceException(Exception):
    """Base exception class for races module."""
    def __init__(self, msg):
        self.msg = msg

ALL_RACES = ('Human',)

def load_race(race):
    """Returns an instance of the named race class.

    Args:
        race (str): case-insensitive name of race to load

    Returns:
        (Race): instance of the appropriate subclass of `Race`
    """
    race = race.capitalize()
    if race in ALL_RACES:
        return globals()[race]()
    else:
        raise RaceException("Invalid race specified.")

def apply_race(char, race):
    """Causes a Character to "become" the named race.

    Args:
        char (Character): the character object becoming a member of race
        race (str, Race): the name of the race to apply, or the
    """
    # if objects are passed in, reload Race and Focus objects
    # by name to ensure we have un-modified versions of them
    if isinstance(race, Race):
        race = race.name

    race = load_race(race)

    # set race and related attributes on the character
    char.db.race = race.name
    char.db.slots = race.slots
    char.db.limbs = race.limbs

    # apply race-based bonuses
    for trait, bonus in race.bonuses.iteritems():
        char.traits[trait].mod += bonus


def _format_bonuses(bonuses):
    """Formats a dict of bonuses to base traits as a string."""
    traits = bonuses.keys()
    if len(bonuses) > 2:
        output = ", ".join(
                    "{{w{:+1}{{n to {{C{}{{n".format(bonuses[t],
                                                     _ARC.traits[t]['name'])
                    for t in traits[:-1])
        output += ", and {{w{:+1}{{n to {{C{}{{n".format(
                      bonuses[traits[-1]],
                      _ARC.traits[traits[-1]]['name'])
    else:
        output = " and ".join(
                    "{{w{:+1}{{n to {{C{}{{n".format(bonuses[t],
                                                     _ARC.traits[t]['name'])
                    for t in traits)
    return output


class Race(object):
    """Base class for race attributes"""
    def __init__(self):
        self.name = ""
        self.plural = "" # Not set on character.
        self.size = ""
        self._desc = ""
        self.slots = {
            'wield1': None,
            'wield2': None,
            'armor': None,
        }
        self.limbs = (
            ('r_arm', ('wield1',)),
            ('l_arm', ('wield2',)),
            ('body', ('armor',)),
        )
        self.foci = []
        self.bonuses = {}

    @property
    def desc(self):
        """Returns a formatted description of the Race.

        Note:
            The setter for this property only modifies the content
            of the first paragraph of what is returned.
        """
        desc = "|g{}|n\n".format(self.name)
        desc += fill(self._desc)
        desc += '\n\n'
        desc += fill("{} have a ".format(self.plural) +
                     "|y{}|n body type.".format(self.size))
        if self.foci:
            desc += fill(
                "They are known for their {}.".format(
                    self._format_focus_list(self.foci)
                )
            )
        if len(self.bonuses) > 0:
            desc += '\n\n'
            desc += fill("{} gain {} of {}".format(
                        self.plural,
                        'bonuses' if len(self.bonuses) > 1 else 'a bonus',
                        _format_bonuses(self.bonuses))
                    )
        desc += '\n\n'
        return desc

    @desc.setter
    def desc(self, value):
        self._desc = value

    def _format_focus_list(self, items):
        """Returns a comma separated list of items with "or" before the last."""
        if len(items) > 2:
            output = ", ".join(["|b{}|n".format(i.name) for i in items[:-1]])
            output += ", and {{b{}{{n".format(items[-1].name)
        else:
            output = " and ".join(["|b{}|n".format(i.name) for i in items])
        return output

class Human(Race):
    """Class representing human attributes."""
    def __init__(self):
        super(Human, self).__init__()
        self.name = "Human"
        self.plural = "Humans"
        self.size = "medium"
        self.desc = ("|gHumans|n are the most widespread of all the races. "
                     "The human traits of curiosity, resourcefulness and "
                     "unyielding courage have helped them to adapt, survive "
                     "and prosper in every world they have explored.")
        self.foci = []
        self.bonuses = {}  #


class Elf(Race):
    """Class representing elf attributes."""
    def __init__(self):
        super(Elf, self).__init__()
        self.name = "Elf"
        self.plural = "Elves"
        self.size = "medium"
        self.desc = ("|gElves|n are graceful, slender demi-humans with delicate "
                     "features and pointy ears. Elves are known to use magic "
                     "spells, but prefer to spend their time feasting and "
                     "frolicking in wooded glades. They rarely visit cities of "
                     "men. Elves are fascinated by magic and never grow weary "
                     "of collecting spells or magic items. Elves love "
                     "beautifully crafted items and choose to live an agrarian "
                     "life in accord with nature. ")
        self.foci = ['agility', 'spirit', 'alertness']
        self.bonuses = {}


class Dwarf(Race):
    """Class representing dwarf attributes."""
    def __init__(self):
        super(Dwarf, self).__init__()
        self.name = "Dwarf"
        self.plural = "Dwarves"
        self.size = "small"
        self.desc = ("|gDwarves|n are short, stocky demi-humans with long, "
                     "respectable beards and heavy stout bodies. Their skin "
                     "is earthen toned and their hair black, gray or dark "
                     "brown. Stubborn but practical; dwarves love grand "
                     "feasts and strong ale. They can be dangerous opponents, "
                     "able to fight with any weapon, melee or ranged. They "
                     "admire craftsmanship and are fond of gold and stonework. "
                     "Dwarves are dependable fighters and sturdy against "
                     "magical influences. ")
        self.foci = ['brawn', 'resilience', 'alertness']
        self.bonuses = {'WILL': 1}
