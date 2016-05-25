from evennia.utils.test_resources import EvenniaTest
from evennia.utils.spawner import spawn

from typeclasses.characters import Character
from typeclasses.weapons import Weapon, TwoHandedWeapon
from world import equip
from world import races
from world.content.prototypes_weapons import SURVIVAL_KNIFE, COLLAPSIBLE_STAFF

class EquipHandlerTestCase(EvenniaTest):
    character_typeclass = Character

    def setUp(self):
        super(EquipHandlerTestCase, self).setUp()
        self.staff = spawn(COLLAPSIBLE_STAFF).pop()
        self.knife = spawn(SURVIVAL_KNIFE).pop()
        races.apply_race(self.char1, races.Human())

    def test_init(self):
        eh = self.char1.equip
        exp_limbs = ['body', 'r_arm', 'l_arm']
        for exp in exp_limbs:
            self.assertIn(exp, eh.limbs)
        exp_slots = ['armor', 'wield1', 'wield2']
        for exp in exp_slots:
            self.assertIn(exp, eh.slots)

    def test_empty_slots(self):
        self.assertEqual(3, len(self.char1.equip.empty_slots))
        self.char1.equip.add(self.knife)
        self.assertNotIn('wield1', self.char1.equip.empty_slots)
        self.char1.equip.remove(self.knife)
        self.assertIn('wield1', self.char1.equip.empty_slots)

    def test_add(self):
        self.assertEqual(3, len(self.char1.equip.empty_slots))
        self.char1.equip.add(self.knife)
        self.assertEqual(self.knife, self.char1.equip.get('wield1'))
        self.char1.equip.remove(self.knife)
        self.char1.equip.add(self.staff)
        self.assertEqual(1, len(self.char1.equip.empty_slots))

    def test_get(self):
        self.assertIsNone(self.char1.equip.get('wield1'))
        self.char1.equip.add(self.staff)
        self.assertEqual(self.staff, self.char1.equip.get('wield2'))

