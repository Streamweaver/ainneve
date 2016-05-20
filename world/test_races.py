"""
Unit tests for the races module.
"""

from unittest import skip
from django.test import TestCase
from evennia.utils.test_resources import EvenniaTest
from typeclasses.characters import Character
from world.archetypes import apply_archetype, calculate_secondary_traits
from world import races

class LoadRaceTestCase(TestCase):

    def test_load_race(self):
        self.assertIsInstance(races.load_race("human"), races.Race)
        self.assertRaises(races.RaceException, races.load_race, "dwarf")

class ApplyRaceTestCase(EvenniaTest):
    character_typeclass = Character

    def test_apply_race(self):
        races.apply_race(self.char1, races.Human())
        self.assertEqual(self.char1.db.race, "Human")
        self.assertIn('wield1', self.char1.db.slots.keys())
        self.assertIn('r_arm', [l[0] for l in self.char1.db.limbs])

class RaceTestCase(TestCase):
    """Test case for Race classes."""
    def test_load_human(self):
        """test that `load_race` loads Human race class"""
        h = races.load_race('human')
        self.assertEqual(h.name, 'Human')

