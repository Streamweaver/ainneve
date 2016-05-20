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


# global skill data is minimal, and can just be stored in a dict for now
_SKILL_DATA = {
    # AGILITY SKILLS
    "dodge": {
        "name": "Dodge",
        "trait": "AGL",
        "desc": "Skill at ducking and avoiding attacks."
    },
    "rifles": {
        "name": "Rifles",
        "trait": "AGL",
        "desc": "Skill at shooting all kind of rifles."
    },
    "melee": {
        "name": "Melee",
        "trait": "AGL",
        "desc": "Skill with melee weapons"
    },
    "heavy weapons": {
        "name": "Heavy Weapons",
        "trait": "AGL",
        "desc": "Skill at using missile launchers and crewed weapons."
    },
    "sleight of hand": {
        "name": "Sleight of Hand",
        "trait": "AGL",
        "desc": "Skill at picking pockets and physical misdirection."
    },
    "throwing": {
        "name": "Throwing",
        "trait": "AGL",
        "desc": "Skill at throwing weapons and grenades."
    },
    # STRENGTH
    "armor": {
        "name": "Armor",
        "trait": "STR",
        "desc": "Skill at wearing non-powered armors."
    },
    "brawling": {
        "name": "Brawling",
        "trait": "STR",
        "desc": "Skill in hand to hand combat."
    },
    # KNWLEGE SKILLS
    "astrography": {
        "name": "Astrography",
        "trait": "KNW",
        "desc": "Skill in stellar mapping and plotting jumps."
    },
    "bureaucracy": {
        "name": "Bureaucracy",
        "trait": "KNW",
        "desc": "Skill in manipulating or examining records, official requests."
    },
    "business": {
        "name": "Business",
        "trait": "KNW",
        "desc": "Skill at trading, negotiating business deals and finding profit."
    },
    "cultures": {
        "name": "Cultures",
        "trait": "KNW",
        "desc": "Understanding of cultures and diplomacy to avoid conflict."
    },
    "intimidation": {
        "name": "Intimidation",
        "trait": "KNW",
        "desc": "Skill at getting others to back down or force them to obey."
    },
    "languages": {
        "name": "Languages",
        "trait": "KNW",
        "desc": "Skill at understanding and deciphering languages"
    },
    "scholar": {
        "name": "Scholar",
        "trait": "KNW",
        "desc": "Skill at examining artifacts or scientific samples."
    },
    "streetwise": {
        "name": "Streetwise",
        "trait": "KNW",
        "desc": "Skill at underworld negotiations, uncovering rumors and finding the black market."
    },
    "survival": {
        "name": "Survival",
        "trait": "KNW",
        "desc": "Skill at enduring and avoiding damage in hostile environments."
    },
    # MCHANICAL SKILLS
    "powered armor": {
        "name": "Powered Armor",
        "trait": "MCH",
        "desc": "Skill at operating powered armor and exoskeletons."
    },
    "gunnery": {
        "name": "Gunnery",
        "trait": "MCH",
        "desc": "Skill operating vehicle mounted weapons."
    },
    "navigation": {
        "name": "Navigation",
        "trait": "MCH",
        "desc": "Skill at plotting courses."
    },
    "piloting": {
        "name":  "piloting",
        "trait": "MCH",
        "desc": "Skill at operating starships and atmospheric vehicles."
    },
    "sensors":  {
        "name": "Sensors",
        "trait": "MCH",
        "desc":  "Skill operating starship or vehicle sensors and cloaks."
    },
    "shields": {
        "name": "Shields",
        "trait": "MCH",
        "desc": "Skill at operating shields."
    },
    # PERCEPTION SKILLS
    "bargain": {
        "name": "Bargain",
        "trait": "PER",
        "desc": "Skill at negotiting prices when buying and selling."
    },
    "gambling": {
        "name": "Gambling",
        "trait": "PER",
        "desc": "Skill at games of chance and high stakes games."
    },
    "stealth": {
        "name": "Stealth",
        "trait": "PER",
        "desc": "Skill at hiding or moving while remaining undetected."
    },
    "investigation": {
        "name":  "Investigation",
        "trait": "PER",
        "desc": "Skill at examining evidence to gain bonuses or information."
    },
    "persuasion": {
        "name": "Persuasion",
        "trait": "PER",
        "desc": "Skill at convincing others."
    },
    "search": {
        "name": "Search",
        "trait": "PER",
        "desc": "Skill at examining areas for hidden items."
    },
    # TCHNICAL SKILLS
    "armorer": {
        "name": "Armorer",
        "trait": "TCH",
        "desc": "Skill at repairing, improving or salvaging armor."
    },
    "computers": {
        "name": "Computers",
        "trait": "TCH",
        "desc": "Skill at operating, and hacking computers."
    },
    "demolitions": {
        "name": "Demolitions",
        "trait": "TCH",
        "desc": "Skill setting or disarming explosives."
    },
    "power armor tech": {
        "name": "Power Armor tech",
        "trait": "TCH",
        "desc": "Skill at repairing, improving or salvaging power armor."
    },
    "gunsmith": {
        "name": "gunsmith",
        "trait": "TCH",
        "desc": "Skill at repairing, improving or salvaging firearms."
    },
    "starship engineering": {
        "name": "Starship Engineering",
        "trait": "TCH",
        "desc": "Skill at repairing, improving or salvaging starships."
    },
    "gunnary tech": {
        "name": "Gunnary tech",
        "trait": "TCH",
        "desc": "Skill at repairing, improving or salvaging vehicle mounted weapons."
    },
    "medicine": {
        "name": "Medicine",
        "trait": "TCH",
        "desc": "Skill at healing and operating medical devices and scanners."
    },
    "robotics": {
        "name": "Robotics",
        "trait": "TCH",
        "desc": "Skill at repairing, improving or salvaing robotics and cybernetics. "
    },
    "security": {
        "name": "Security",
        "trait": "TCH",
        "desc": "Skill at breaching security systems and locks."
    }
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

