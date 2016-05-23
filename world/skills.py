"""
Skills module.

This module contains data and functions related to character Skills.
Skills in D6 are treated as an extension of controlling trait and the
value of the trait and the skill are added together to determine the
final value to roll.  Rolls are checked against a target number difficulty

Skills are stored as world.trait.Trait objects with the governing trait
storedin the extra attribute and accessed like so:

    `> char.skills.athletics.trait`
    `> 'AGL' `

Its public module functions are to be used primarily during the character
creation process.

Classes:

    `Skill`: convenience object for skill display data

Module Functions:

    - `apply_skills(char)`

        Initializes a character's db.skills attribute to support skill
        traits. In OA, all skills start matching their base trait before
        the player allocates a number of +1 and -1 counters.

    - `load_skill(skill)`

        Loads an instance of the Skill class by name for display of
        skill name and description.

    - `validate_skills(char)`

        Validates a player's skill penalty and bonus token allocations.
        Because the requirements depend on the char's INT trait, it
        accepts the entire char as its argument.

    - `finalize_skills(skills)`

        Finalizes and "saves" the player's allocations and deletes the
        'plus' and 'minus' extra keys used during chargen.
"""
from math import ceil

class SkillException(Exception):
    def __init__(self, msg):
        self.msg = msg


# Produces from /scripts file prasing of my csv
# global skill data is minimal, and can just be stored in a dict for now
_SKILL_DATA = {
    "dodge": {
        'name': "Dodge",
        "trait": "AGL",
        "desc": "Adds to the difficulty to hit you in personal combat.",
        "initial": 0
    },

    "energy_pistol": {
        'name': "Energy Pistol",
        "trait": "AGL",
        "desc": "Use of laser or plasma pistols.",
        "initial": 0
    },

    "energy_rifle": {
        'name': "Energy Rifle",
        "trait": "AGL",
        "desc": "Use of laser or plasma rifles and assualt rifles.",
        "initial": 0
    },

    "pistol": {
        'name': "Pistol",
        "trait": "AGL",
        "desc": "Use of conventional pistols.",
        "initial": 0
    },

    "rifle": {
        'name': "Rifle",
        "trait": "AGL",
        "desc": "Use of conventional rifles and assault rifles.",
        "initial": 0
    },

    "shotgun": {
        'name': "Shotgun",
        "trait": "AGL",
        "desc": "Use of shotguns.",
        "initial": 0
    },

    "throwing": {
        'name': "Throwing",
        "trait": "AGL",
        "desc": "Accuracy when using grenades and other thrown weapons.",
        "initial": 0
    },

    "astrography": {
        'name': "Astrography",
        "trait": "KNW",
        "desc": "Effectiveness at plotting jumps.",
        "initial": None
    },

    "bureaucracy": {
        'name': "Bureaucracy",
        "trait": "KNW",
        "desc": "Effects docking fees and fines.",
        "initial": 0
    },

    "business": {
        'name': "Business",
        "trait": "KNW",
        "desc": "Effects prices when trading goods.",
        "initial": None
    },

    "cultures": {
        'name': "Cultures",
        "trait": "KNW",
        "desc": "Examining cultural artifacts for value.",
        "initial": None
    },

    "intimidation": {
        'name': "Intimidation",
        "trait": "KNW",
        "desc": "Reduce opponents effectiveness in combat or sometimes make them flee.",
        "initial": 0
    },

    "languages": {
        'name': "Languages",
        "trait": "KNW",
        "desc": "Decyphering ancient texts and artifacts.",
        "initial": None
    },

    "scholar": {
        'name': "Scholar",
        "trait": "KNW",
        "desc": "Analyzing sciendific samples for credits.",
        "initial": None
    },

    "streetwise": {
        'name': "Streetwise",
        "trait": "KNW",
        "desc": "Uncover rumors and find the black market.",
        "initial": 0
    },

    "survival": {
        'name': "Survival",
        "trait": "KNW",
        "desc": "Reduce or avoid damage in harsh conditions on marginal worlds.",
        "initial": 0
    },

    "gunnery": {
        'name': "Gunnery",
        "trait": "MCH",
        "desc": "Use of ship mounted direct fire weapons.",
        "initial": 0
    },

    "missile_launchers": {
        'name': "Missile Launchers",
        "trait": "MCH",
        "desc": "Use of ship mounted missile launchers.",
        "initial": None
    },

    "navigation": {
        'name': "Navigation",
        "trait": "MCH",
        "desc": "Effects fuel use and accuracy in plotting courses.",
        "initial": None
    },

    "powered_armor": {
        'name': "Powered Armor",
        "trait": "MCH",
        "desc": "Use of powered armor and exoskeletons.",
        "initial": None
    },

    "sensors": {
        'name': "Sensors",
        "trait": "MCH",
        "desc": "Accuracy and effectiveness of ships sensors and cloaks.",
        "initial": None
    },

    "shields": {
        'name': "Shields",
        "trait": "MCH",
        "desc": "Use of ships shields to resist damage.",
        "initial": None
    },

    "starship_pilot": {
        'name': "Starship Pilot",
        "trait": "MCH",
        "desc": "Flying starships to avoid damage and out menuver other starships.",
        "initial": None
    },

    "bargain": {
        'name': "Bargain",
        "trait": "PER",
        "desc": "Effects prices when buying and selling in stores.",
        "initial": 0
    },

    "persuasion": {
        'name': "Persuasion",
        "trait": "PER",
        "desc": "Chance of getting others to perform actions.",
        "initial": 0
    },

    "search": {
        'name': "Search",
        "trait": "PER",
        "desc": "Success at noticing details or finding hidden items.",
        "initial": 0
    },

    "stealth": {
        'name': "Stealth",
        "trait": "PER",
        "desc": "Chance to avoid detection or notice.",
        "initial": 0
    },

    "armor": {
        'name': "Armor",
        "trait": "STR",
        "desc": "Use of conventional armors.",
        "initial": 0
    },

    "blunt_weapons": {
        'name': "Blunt Weapons",
        "trait": "STR",
        "desc": "Use of blunt weapons of all kinds.",
        "initial": 0
    },

    "hand_to_hand": {
        'name': "Hand To Hand",
        "trait": "STR",
        "desc": "Use of unarmed combat.",
        "initial": 0
    },

    "heavy_weapons": {
        'name': "Heavy Weapons",
        "trait": "STR",
        "desc": "Use of personal missile launchers and crewed weapons.",
        "initial": None
    },

    "knives": {
        'name': "Knives",
        "trait": "STR",
        "desc": "Use of knives and short blades.",
        "initial": 0
    },

    "swords": {
        'name': "Swords",
        "trait": "STR",
        "desc": "Use of swords and energized swords.",
        "initial": 0
    },

    "armorer": {
        'name': "Armorer",
        "trait": "TCH",
        "desc": "Repairing or salvaging conventional armor.",
        "initial": None
    },

    "computers": {
        'name': "Computers",
        "trait": "TCH",
        "desc": "Operating and hacking computers.",
        "initial": 0
    },

    "demolitions": {
        'name': "Demolitions",
        "trait": "TCH",
        "desc": "Usng or disarming explosives.",
        "initial": None
    },

    "gunnary_tech": {
        'name': "Gunnary Tech",
        "trait": "TCH",
        "desc": "Repairing or salvaging ship mounted weapons.",
        "initial": None
    },

    "gunsmith": {
        'name': "Gunsmith",
        "trait": "TCH",
        "desc": "Repairing or salvaging firearms.",
        "initial": None
    },

    "medicine": {
        'name': "Medicine",
        "trait": "TCH",
        "desc": "Healing others and yourself.",
        "initial": 0
    },

    "power_armor_tech": {
        'name': "Power Armor Tech",
        "trait": "TCH",
        "desc": "Repairing or salvaging power armor.",
        "initial": None
    },

    "robotics": {
        'name': "Robotics",
        "trait": "TCH",
        "desc": "Repairing or salvaing robotics and cybernetics. ",
        "initial": None
    },

    "security": {
        'name': "Security",
        "trait": "TCH",
        "desc": "Breaching electronic security systems and locks.",
        "initial": 0
    },

    "starship_engineering": {
        'name': "Starship Engineering",
        "trait": "TCH",
        "desc": "Repairing or salvaging starships.",
        "initial": None
    },
}

# skill groupings used in skills command
ALL_SKILLS = tuple(sorted([name for name in _SKILL_DATA.keys()]))

STR_SKILLS = [s for s in ALL_SKILLS if _SKILL_DATA[s]["trait"] == 'STR']
AGL_SKILLS = [s for s in ALL_SKILLS if _SKILL_DATA[s]["trait"] == 'AGL']
KNW_SKILLS = [s for s in ALL_SKILLS if _SKILL_DATA[s]["trait"] == 'KNW']
MCH_SKILLS = [s for s in ALL_SKILLS if _SKILL_DATA[s]["trait"] == 'MCH']
PER_SKILLS = [s for s in ALL_SKILLS if _SKILL_DATA[s]["trait"] == 'PER']
TCH_SKILLS = [s for s in ALL_SKILLS if _SKILL_DATA[s]["trait"] == 'TCH']


def apply_skills(char, skills):
    """Sets up a character's initial skill traits.

    Args:
        char (Character): the character being initialized
        skills: dict of skills {'skillname': invalue, ... }
    """
    char.skills.clear()
    for skill, value in skills.iteritems():
        if skill.lower() not in _SKILL_DATA.keys():
            raise SkillException("Invalid skill %s." % skill.lower())
        char.skills.add(
            key=skill,
            type='static',
            base=value,
            mod=0,
            name=_SKILL_DATA[skill]["name"],
            extra={'trait': _SKILL_DATA[skill]['trait'], 'is_d6': True}
        )


def load_skill(skill):
    """Retrieves an instance of a `Skill` class.

    Args:
        skill (str): case insensitive skill name

    Returns:
        (Skill): instance of the named Skill
    """
    skill = skill.lower()
    if skill in ALL_SKILLS:
        return Skill(**_SKILL_DATA[skill])
    else:
        raise SkillException('Invalid skill name.')


def validate_skills(char):
    """No longer needed as skills are applied directly from archetype"""
    pass


def finalize_skills(skills):
    """No Longer needed as skills are applied directly from archetype"""
    pass


class Skill(object):
    """Represents a Skill's display attributes for use in chargen.

    Args:
        name (str): display name for skill
        desc (str): description of skill
    """
    def __init__(self, name, desc, trait):
        self.name = name
        self.desc = desc
        self.base = 0
        self.trait = trait

