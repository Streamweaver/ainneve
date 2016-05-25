"""
Prototype module containing weapons and shields.
"""

# from evennia.utils import fill

## Weapons from D6
SG16_SHOTGUN = {
    'name': 'SG16 Shotgun',
    'aliases': ['sg16'],
    'typeclass': 'typeclasses.weapons.TwoHandedRanged',
    'desc': 'shotgun',
    'weight': 1,
    'value': 8,
    'damage': 16,
    'wear': 0,
    'durability': 5,
    'bonus': 0,
    'use_skill': 'shotgun',
    'fix_skill': 'gunsmith',
        }

P11_PISTOL = {
    'name': 'P11 Pistol',
    'aliases': ['p11'],
    'typeclass': 'typeclasses.weapons.RangedWeapon',
    'desc': 'Hand held pistol.',
    'weight': 1,
    'value': 7,
    'damage': 11,
    'wear': 0,
    'durability': 5,
    'bonus': 0,
    'use_skill': 'pistol',
    'fix_skill': 'gunsmith',
        }

R16_RIFLE = {
    'name': 'R16 Rifle',
    'aliases': ['r16'],
    'typeclass': 'typeclasses.weapons.TwoHandedRanged',
    'desc': 'Long conventional rifel.',
    'weight': 1,
    'value': 9,
    'damage': 16,
    'wear': 0,
    'durability': 5,
    'bonus': 0,
    'use_skill': 'rifle',
    'fix_skill': 'gunsmith',
        }

LR14_LASER_RIFLE = {
    'name': 'LR14 Laser Rifle',
    'aliases': ['lr14'],
    'typeclass': 'typeclasses.weapons.TwoHandedRanged',
    'desc': 'Fires a focuse energy beam.',
    'weight': 1,
    'value': 15,
    'damage': 14,
    'wear': 0,
    'durability': 5,
    'bonus': 0,
    'use_skill': 'energy_rifle',
    'fix_skill': 'gunsmith',
        }

PR21_PLASMA_RIFLE = {
    'name': 'PR21 Plasma Rifle',
    'aliases': ['pr21'],
    'typeclass': 'typeclasses.weapons.TwoHandedRanged',
    'desc': 'Fires contained blasts of plasma.',
    'weight': 1,
    'value': 18,
    'damage': 21,
    'wear': 0,
    'durability': 5,
    'bonus': 0,
    'use_skill': 'energy_pistol',
    'fix_skill': 'gunsmith',
        }

LP12_LASER_PISTOL = {
    'name': 'LP12 Laser Pistol',
    'aliases': ['lp12'],
    'typeclass': 'typeclasses.weapons.RangedWeapon',
    'desc': 'Hand held pistol that fires focused beam of energy.',
    'weight': 1,
    'value': 14,
    'damage': 12,
    'wear': 0,
    'durability': 5,
    'bonus': 0,
    'use_skill': 'energy_pistol',
    'fix_skill': 'gunsmith',
        }

PP15_PLASMA_PISTOL = {
    'name': 'PP15 Plasma Pistol',
    'aliases': ['pp15'],
    'typeclass': 'typeclasses.weapons.RangedWeapon',
    'desc': 'Hand held pistol that fires a contained blast of plasma.',
    'weight': 1,
    'value': 15,
    'damage': 15,
    'wear': 0,
    'durability': 5,
    'bonus': 0,
    'use_skill': 'energy_pistol',
    'fix_skill': 'gunsmith',
        }

SURVIVAL_KNIFE = {
    'name': 'survival knife',
    'aliases': ['knife'],
    'typeclass': 'typeclasses.weapons.Weapon',
    'desc': 'Composite carbon blade with a mono-thin edge.',
    'weight': 1,
    'value': 3,
    'damage': 3,
    'wear': 0,
    'durability': 5,
    'bonus': 0,
    'use_skill': 'knives',
    'fix_skill': 'gunsmith',
        }

MONOSWORD = {
    'name': 'monosword',
    'aliases': [],
    'typeclass': 'typeclasses.weapons.Weapon',
    'desc': 'Light composite carbon blade about half a meter long.',
    'weight': 1,
    'value': 8,
    'damage': 9,
    'wear': 0,
    'durability': 5,
    'bonus': 0,
    'use_skill': 'swords',
    'fix_skill': 'gunsmith',
        }

ENERGY_BATON = {
    'name': 'energy baton',
    'aliases': [],
    'typeclass': 'typeclasses.weapons.Weapon',
    'desc': 'Baton that releases a shock on impact.',
    'weight': 1,
    'value': 6,
    'damage': 5,
    'wear': 0,
    'durability': 5,
    'bonus': 0,
    'use_skill': 'blunt_weapons',
    'fix_skill': 'gunsmith',
        }

COLLAPSIBLE_STAFF = {
    'name': 'collapsible staff',
    'aliases': ['staff'],
    'typeclass': 'typeclasses.weapons.TwoHandedWeapon',
    'desc': 'Dark carbon staff that seems smooth but can collapse and expand on command.',
    'weight': 1,
    'value': 7,
    'damage': 6,
    'wear': 0,
    'durability': 5,
    'bonus': 0,
    'use_skill': 'blunt_weapons',
    'fix_skill': 'gunsmith',
        }

VIBROSWORD = {
    'name': 'vibrosword',
    'aliases': [],
    'typeclass': 'typeclasses.weapons.Weapon',
    'desc': 'Monosword that increases cutting power through microvibrations.',
    'weight': 1,
    'value': 18,
    'damage': 12,
    'wear': 0,
    'durability': 5,
    'bonus': 0,
    'use_skill': 'swords',
    'fix_skill': 'gunsmith',
        }

SMG14_SUBMACHINE_GUN = {
    'name': 'SMG14 Submachine Gun',
    'aliases': ['smg', 'smg14'],
    'typeclass': 'typeclasses.weapons.RangedWeapon',
    'desc': 'Large autopistol.',
    'weight': 1,
    'value': 10,
    'damage': 14,
    'wear': 0,
    'durability': 5,
    'bonus': 0,
    'use_skill': 'pistol',
    'fix_skill': 'gunsmith',
        }

AR18_ASSAULT_RIFLE = {
    'name': 'AR18 Assault Rifle',
    'aliases': ['ar18'],
    'typeclass': 'typeclasses.weapons.TwoHandedRanged',
    'desc': 'Multi-modal combat rifle.',
    'weight': 1,
    'value': 18,
    'damage': 18,
    'wear': 0,
    'durability': 5,
    'bonus': 0,
    'use_skill': 'rifle',
    'fix_skill': 'gunsmith',
        }
