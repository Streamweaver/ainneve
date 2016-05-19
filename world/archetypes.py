"""
Ainneve archetypes module.

This module encapsulates archetype-related data including character
trait definitions, and eventually default ability stats and OA talents to
select from when leveling up.

Archetype classes are meant to be loaded by name as needed to provide access
to archetype-specific data, not to be saved on a `Character` object. Only
the archetype name is stored in the character's `db` attribute handler,
and that value is generally set by the `apply_archetype` module function.

Module Functions:

    - `apply_archetype(char, name, reset=False)`

        Causes character `char` to become archetype `name`. Initializes db
        attributes on `char` to archetype defaults. Can be called twice on
        the same character with two different `name` parameters to create
        a dual archetype. May also be called with reset=True to remove
        any existing archetype and initialize the character with only the
        named one.

    - `get_remaining_allocation(traits)`

        Returns the nummber of trait points left for the player to allocate
        to primary traits.

    - `validate_primary_traits(traits)`

        Confirms that all primary traits total 30 points, and all but MAG
        are at least 1 and no greater than 10.

    - `calculate_secondary_traits(traits)`

        Called to set initial base values for secondary traits and save
        rolls.

    - `finalize_traits(traits)`

        Called at the end of chargen to apply modifiers to base values and
        reset `mod` values for normal game play.

    - `load_archetype(name)`

        Returns an instance of the named Archetype class.
"""

from world.rulebook import roll_max
from evennia.utils import fill
from evennia.utils.evtable import EvTable


class ArchetypeException(Exception):
    def __init__(self, msg):
        self.msg = msg

ARCHETYPE_DATA = {
    'soldier': {
        'name': 'Soldier',
        'AGL': 12, 'STR': 12, 'KNW': 7, 'MCH': 8, 'PER': 8, 'TCH': 7,
        'desc': fill(
            "|cSoldiers|n are highly skilled in many forms of combat.  They can "
            "be military veterans, mercinaries, security forces or anyone with "
            "professional military experience. "
        )
    },
    'scout': {
        'name': 'Scout',
        'AGL': 8, 'STR': 7, 'KNW': 11, 'MCH': 11, 'PER': 8, 'TCH': 9,
        'desc': "|cScouts|n are explorers, independent pilots and all around survivalists."
    },
    'scoundrel': {
        'name': 'Scoundrels',
        'AGL': 11, 'STR': 6, 'KNW': 9, 'MCH': 9, 'PER': 13, 'TCH': 6,
        'desc': "|cScoundrels|n are con-men, gamblers, crime lords and fixers."
    }
}

PRIMARY_TRAITS = ('AGL', 'STR', 'KNW', 'MCH', 'PER','TCH')
SECONDARY_TRAITS = ('WOUNDS', 'FATE')
PSIONIC_TRAITS = ('MP',) # Save for later
# COMBAT_TRAITS = ('ATKM', 'ATKR', 'ATKU', 'DEF', 'PP')
OTHER_TRAITS = ('CP', 'ENC')

ALL_TRAITS = (PRIMARY_TRAITS + SECONDARY_TRAITS + OTHER_TRAITS) # ADD psionics later

TOTAL_PRIMARY_POINTS = 54

def apply_archetype(char, name, reset=False):
    """Set a character's archetype and initialize traits.

    Used during character creation; initializes the traits collection. It
    can be called twice to make the character a Dual-Archetype.

    Args:
        char (Character): the character being initialized.
        name (str): single archetype name to apply. If the character already
            has a single archetype, it is combined with the existing as a
            dual archetype.
        reset (bool): if True, remove any current archetype and apply the
            named archetype as new.
    """
    # print("\n".join[name, "%s" % VALID_ARCHETYPES])
    name = name.lower()
    if name not in ARCHETYPE_DATA:
        raise ArchetypeException('Invalid archetype.')

    if char.db.archetype is not None and not reset:
        raise ArchetypeException('Character is already a {}'.format(name))
    if name not in ARCHETYPE_DATA:
        raise AttributeError("No archetype defined for {}".format(name))
    archetype = load_archetype(name)
    char.db.archetype = archetype.name
    if reset:
        char.traits.clear()
    for key, kwargs in archetype.traits.iteritems():
        char.traits.add(key, **kwargs)


def get_remaining_allocation(traits):
    """Returns the number of trait points remaining to be assigned.

    Args:
        traits (TraitHandler): Partially loaded TraitHandler

    Returns:
        (int): number of trait points left for the player to allocate
    """
    allocated = sum(traits[t].actual for t in PRIMARY_TRAITS)
    return TOTAL_PRIMARY_POINTS - allocated


def validate_primary_traits(traits):
    """Validates proposed primary trait allocations during chargen.

    Args:
        traits (TraitHandler): TraitHandler loaded with proposed final
            primary traits

    Returns:
        (tuple[bool, str]): first value is whether the traits are valid,
            second value is error message
    """
    total = sum(traits[t].actual for t in PRIMARY_TRAITS)
    if total > TOTAL_PRIMARY_POINTS:
        return False, 'Too many trait points allocated.'
    if total < TOTAL_PRIMARY_POINTS:
        return False, 'Not enough trait points allocated.'
    else:
        return True, None


def calculate_secondary_traits(traits):
    """Calculates secondary traits

    Args:
        traits (TraitHandler): factory attribute with primary traits
        populated.
    """
    # secondary traits
    pass # we don't do this in this implementation. May need if I move to bodypoints


def finalize_traits(traits):
    """Applies all pending modifications to starting traits.

    During the chargen process, race-based bonuses and player
    allocations are applied to trait modifiers. This function
    applies any `mod` values to the traits' `base`, then resets
    the `mod` property.
    """
    for t in PRIMARY_TRAITS + SECONDARY_TRAITS:
        traits[t].base = traits[t].actual if traits[t].actual >= 1 else 1 # min 1D on anything.
        traits[t].reset_mod()


def load_archetype(name):
    """Loads an instance of the named Archetype class.

    Args:
        name (str): Name of either single or dual-archetype

    Return:
        (Archetype): An instance of the requested archetype class.
    """
    name = name.lower()
    try:
        data = ARCHETYPE_DATA[name].copy()
        archetype = Archetype(data)
    except KeyError:
        raise ArchetypeException("No data found for {}".format(name))

    return archetype

# Archetype Classes


class Archetype(object):
    """Base archetype class containing default values for all traits."""
    def __init__(self, data):
        try:
            self.name = data['name']
            self._desc = data['desc']
            self.traits = {
                # primary
                'AGL': {'type': 'static', 'base': data['AGL'], 'mod': 0, 'name': 'Agility'},
                'STR': {'type': 'static', 'base': data['STR'], 'mod': 0, 'name': 'Strength'},
                'KNW': {'type': 'static', 'base': data['KNW'], 'mod': 0, 'name': 'Knowledge'},
                'TCH': {'type': 'static', 'base': data['TCH'], 'mod': 0, 'name': 'Technical'},
                'PER': {'type': 'static', 'base': data['PER'], 'mod': 0, 'name': 'Perception'},
                'MCH': {'type': 'static', 'base': data['MCH'], 'mod': 0, 'name': 'Mechanical'},
                # secondary
                'WOUNDS': {'type': 'static', 'base': 0, 'mod': 0, 'min': 0, 'max': 6, 'name': 'Wounds'},
                'FATE': {'type': 'static', 'base': 0, 'mod': 0, 'name': 'Fate'},
                # misc
                'ENC': {'type': 'counter', 'base': 0, 'mod': 0, 'min': 0, 'name': 'Carry Weight'},
                'CP': {'type': 'static', 'base': 0, 'mod': 0, 'name': 'Character Points'},
            }
        except KeyError:
            raise ArchetypeException("Archetype data invalid.")

    @property
    def ldesc(self):
        """Returns a formatted description of the Archetype."""
        desc = "Archetype: |c{archetype}|n\n"
        desc += '~' * (11 + len(self.name)) + '\n'
        desc += self.desc
        desc += '\n\n'
        desc += "|c{archetype}s|n start with the following base primary traits:"
        desc += "\n{traits}\n"

        data = []
        for i in xrange(3):
            data.append([self._format_trait_3col(self.traits[t])
                         for t in PRIMARY_TRAITS[i::3]])
        traits = EvTable(header=False, table=data)

        return desc.format(archetype=self.name,
                           traits=traits)

    @property
    def desc(self):
        """The narrative description of the Archetype."""
        return self._desc

    @desc.setter
    def desc(self, desc):
        self._desc = desc

    def _format_trait_3col(self, trait):
        """Return a trait : value pair formatted for 3col layout"""
        return "|C{:<16.16}|n : |w{:>3}|n".format(
                    trait['name'], trait['base']) # TODO trait['base'] needs to be wrapped in a d6 formatter
