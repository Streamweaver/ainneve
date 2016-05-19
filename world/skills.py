"""
Skills module.

This module contains data and functions related to character Skills.
Skills in OA are treated as a modifier to a standard roll that is
typically compared to a target number of 5, though that can vary for
some skills.

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


# global skill data is minimal, and can just be stored in a dict for now
_SKILL_DATA = {
    # AGILITY SKILLS
    "dodge": {
        "name": "Dodge",
        "base": "AGL",
        "desc": "Skill at ducking and avoiding attacks."
    },
    "rifles": {
        "name": "Rifles",
        "base": "AGL",
        "desc": "Skill at shooting all kind of rifles."
    },
    "melee": {
        "name": "Melee",
        "base": "AGL",
        "desc": "Skill with melee weapons"
    },
    "heavy weapons": {
        "name": "Heavy Weapons",
        "base": "AGL",
        "desc": "Skill at using missile launchers and crewed weapons."
    },
    "sleight of hand": {
        "name": "Sleight of Hand",
        "base": "AGL",
        "desc": "Skill at picking pockets and physical misdirection."
    },
    "throwing": {
        "name": "Throwing",
        "base": "AGL",
        "desc": "Skill at throwing weapons and grenades."
    },
    # STRENGTH
    "armor": {
        "name": "Armor",
        "base": "STR",
        "desc": "Skill at wearing non-powered armors."
    },
    "brawling": {
        "name": "Brawling",
        "base": "STR",
        "desc": "Skill in hand to hand combat."
    },
    # KNWLEGE SKILLS
    "astrography": {
        "name": "Astrography",
        "base": "KNW",
        "desc": "Skill in stellar mapping and plotting jumps."
    },
    "bureaucracy": {
        "name": "Bureaucracy",
        "base": "KNW",
        "desc": "Skill in manipulating or examining records, official requests."
    },
    "business": {
        "name": "Business",
        "base": "KNW",
        "desc": "Skill at trading, negotiating business deals and finding profit."
    },
    "cultures": {
        "name": "Cultures",
        "base": "KNW",
        "desc": "Understanding of cultures and diplomacy to avoid conflict."
    },
    "intimidation": {
        "name": "Intimidation",
        "base": "KNW",
        "desc": "Skill at getting others to back down or force them to obey."
    },
    "languages": {
        "name": "Languages",
        "base": "KNW",
        "desc": "Skill at understanding and deciphering languages"
    },
    "scholar": {
        "name": "Scholar",
        "base": "KNW",
        "desc": "Skill at examining artifacts or scientific samples."
    },
    "streetwise": {
        "name": "Streetwise",
        "base": "KNW",
        "desc": "Skill at underworld negotiations, uncovering rumors and finding the black market."
    },
    "survival": {
        "name": "Survival",
        "base": "KNW",
        "desc": "Skill at enduring and avoiding damage in hostile environments."
    },
    # MCHANICAL SKILLS
    "powered armor": {
        "name": "Powered Armor",
        "base": "MCH",
        "desc": "Skill at operating powered armor and exoskeletons."
    },
    "gunnery": {
        "name": "Gunnery",
        "base": "MCH",
        "desc": "Skill operating vehicle mounted weapons."
    },
    "navigation": {
        "name": "Navigation",
        "base": "MCH",
        "desc": "Skill at plotting courses."
    },
    "piloting": {
        "name":  "piloting",
        "base": "MCH",
        "desc": "Skill at operating starships and atmospheric vehicles."
    },
    "sensors":  {
        "name": "Sensors",
        "base": "MCH",
        "desc":  "Skill operating starship or vehicle sensors and cloaks."
    },
    "shields": {
        "name": "Shields",
        "base": "MCH",
        "desc": "Skill at operating shields."
    },
    # PERCEPTION SKILLS
    "bargain": {
        "name": "Bargain",
        "base": "PER",
        "desc": "Skill at negotiting prices when buying and selling."
    },
    "gambling": {
        "name": "Gambling",
        "base": "PER",
        "desc": "Skill at games of chance and high stakes games."
    },
    "stealth": {
        "name": "Stealth",
        "base": "PER",
        "desc": "Skill at hiding or moving while remaining undetected."
    },
    "investigation": {
        "name":  "Investigation",
        "base": "PER",
        "desc": "Skill at examining evidence to gain bonuses or information."
    },
    "persuasion": {
        "name": "Persuasion",
        "base": "PER",
        "desc": "Skill at convincing others."
    },
    "search": {
        "name": "Search",
        "base": "PER",
        "desc": "Skill at examining areas for hidden items."
    },
    # TCHNICAL SKILLS
    "armorer": {
        "name": "Armorer",
        "base": "TCH",
        "desc": "Skill at repairing, improving or salvaging armor."
    },
    "computers": {
        "name": "Computers",
        "base": "TCH",
        "desc": "Skill at operating, and hacking computers."
    },
    "demolitions": {
        "name": "Demolitions",
        "base": "TCH",
        "desc": "Skill setting or disarming explosives."
    },
    "power armor tech": {
        "name": "Power Armor tech",
        "base": "TCH",
        "desc": "Skill at repairing, improving or salvaging power armor."
    },
    "gunsmith": {
        "name": "gunsmith",
        "base": "TCH",
        "desc": "Skill at repairing, improving or salvaging firearms."
    },
    "starship engineering": {
        "name": "Starship Engineering",
        "base": "TCH",
        "desc": "Skill at repairing, improving or salvaging starships."
    },
    "gunnary tech": {
        "name": "Gunnary tech",
        "base": "TCH",
        "desc": "Skill at repairing, improving or salvaging vehicle mounted weapons."
    },
    "medicine": {
        "name": "Medicine",
        "base": "TCH",
        "desc": "Skill at healing and operating medical devices and scanners."
    },
    "robotics": {
        "name": "Robotics",
        "base": "TCH",
        "desc": "Skill at repairing, improving or salvaing robotics and cybernetics. "
    },
    "security": {
        "name": "Security",
        "base": "TCH",
        "desc": "Skill at breaching security systems and locks."
    }
}

# skill groupings used in skills command
ALL_SKILLS = tuple(sorted([name for name in _SKILL_DATA.keys()]))

STR_SKILLS = [s for s in ALL_SKILLS if _SKILL_DATA[s]['base'] == 'STR']
AGL_SKILLS = [s for s in ALL_SKILLS if _SKILL_DATA[s]['base'] == 'AGL']
KNW_SKILLS = [s for s in ALL_SKILLS if _SKILL_DATA[s]['base'] == 'KNW']
MCH_SKILLS = [s for s in ALL_SKILLS if _SKILL_DATA[s]['base'] == 'MCH']
PER_SKILLS = [s for s in ALL_SKILLS if _SKILL_DATA[s]['base'] == 'PER']
TCH_SKILLS = [s for s in ALL_SKILLS if _SKILL_DATA[s]['base'] == 'TCH']


def apply_skills(char):
    """Sets up a character's initial skill traits.

    Args:
        char (Character): the character being initialized
    """
    char.skills.clear()
    for skill, data in _SKILL_DATA.iteritems():
        char.skills.add(
            key=skill,
            type='static',
            base=char.traits[data['base']].actual,
            mod=0,
            name=data['name'],
            extra=dict(plus=0, minus=0)
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
    """Validates a player's skill allocations during chargen.

    Args:
        char (Character): character with populated skills TraitHandler

    Returns:
        (tuple[bool, str]): first value is whether the skills are valid,
            second value is error message
    """
    minus_count = 3
    plus_count = ceil(char.traits.INT.actual / 3.0)
    if sum(char.skills[s].minus for s in ALL_SKILLS) != minus_count:
        return False, 'Not enough -1 counters allocated.'
    if sum(char.skills[s].plus for s in ALL_SKILLS) != plus_count:
        return False, 'Not enough +1 counters allocated.'
    return True, ''


def finalize_skills(skills):
    """Sets/calculates the permanent skill values at the end of chargen.

    Args:
        skills (TraitHandler): validated skills TraitHandler collection

    Note:
        During chargen, penalty counters are applied to the `base`
        property, and bonus counters to the `mod`. This function is
        called after validation to set the combined values as `base`
        and reset `mod` to zero for game play.
    """
    for skill in ALL_SKILLS:
        skills[skill].base += skills[skill].plus
        skills[skill].base -= skills[skill].minus
        del skills[skill].plus
        del skills[skill].minus


class Skill(object):
    """Represents a Skill's display attributes for use in chargen.

    Args:
        name (str): display name for skill
        desc (str): description of skill
    """
    def __init__(self, name, desc, base):
        self.name = name
        self.desc = desc
        self.base = base

