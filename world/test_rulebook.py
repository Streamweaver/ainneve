"""
Unit tests for world.archetypes module.
"""

from unittest import skip

from evennia.utils.test_resources import EvenniaTest

from utils.utils import d6str
from world import rulebook, skills, archetypes
from typeclasses.characters import Character

class RulebookTestCase(EvenniaTest):
    character_typeclass = Character

    def setUp(self):
        super(RulebookTestCase, self).setUp()
        archetypes.apply_archetype(self.char1, 'soldier')
        skill_list = {
            'dodge': 1,
            'rifles': 0,
            'powered armor': 10,
            'piloting': 5,
        }
        skills.apply_skills(self.char1, skill_list)

    def test_d6roll(self):
        for value in range(3, 16):
            for i in range(1000):
                min = value / 3 + value % 3
                max = value / 3 * 6 + value % 3
                roll = rulebook.d6roll(value)
                self.assertTrue(min <= roll <= max, msg="{} is out or range for {}".format(roll, d6str(value)))

    def test_skill_result(self):
        for _ in range(1000):
            actual = rulebook.skill_result(self.char1,
                                           self.char1.skills['piloting'])
            print(self.char1.skills['piloting'].trait)
            print(self.char1.skills['piloting'].actual)
            print(self.char1.traits.MCH.actual)
            # total value of 13 for this = 4D+1
            self.assertTrue(5 <= actual <= 25, "%i" % actual)