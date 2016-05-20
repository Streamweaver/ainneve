from evennia.utils import fill

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