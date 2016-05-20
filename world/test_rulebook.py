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
        for trait in archetypes.PRIMARY_TRAITS:
            self.char1.traits[trait].base = 8
        skill_list = {
            'dodge': 1,
            'rifles': 0,
            'powered armor': 10,
            'piloting': 5,
        }
        skills.apply_skills(self.char1, skill_list)

    def test_skill_value(self):
        skill = self.char1.skills.piloting
        self.assertEqual(13, rulebook.skill_value(self.char1, skill))

        self.char1.traits.MCH.mod = -3
        self.assertEqual(10, rulebook.skill_value(self.char1, skill))

        self.char1.traits.MCH.reset_mod()
        self.assertEqual(13, rulebook.skill_value(self.char1, skill))

    def test_d6roll(self):
        for value in range(3, 16):
            for i in range(1000):
                min = value / 3 + value % 3
                max = value / 3 * 6 + value % 3
                roll = rulebook.d6roll(value)
                self.assertTrue(min <= roll <= max, msg="{} is out or range for {}".format(roll, d6str(value)))

    def test_skill_result(self):
        rollmin = 100
        rollmax = 0
        for _ in range(1000):
            skill = self.char1.skills.piloting
            actual = rulebook.skill_result(self.char1,
                                           skill)
            # total value of 13 for this = 4D+1
            if actual < rollmin:
                rollmin = actual
            if actual > rollmax:
                rollmax = actual
            self.assertTrue(5 <= actual <= 25, "%i" % actual)
         # it should not spitting out same number
        self.assertNotEqual(rollmin, rollmax)

        # it should return zero on a bad trait name
        skill = self.char1.skills.piloting
        skill.trait = 'PRE'
        actual = rulebook.skill_result(self.char1, skill)
        self.assertEqual(actual, 0)

    def test_skill_check(self):
        for _ in range(1000):
            # TODO refactor range based on getting actual value.
            # piloting 4D+1 for this
            skill = self.char1.skills.piloting
            self.assertTrue(rulebook.skill_check(self.char1, skill, 4))
            self.assertFalse(rulebook.skill_check(self.char1, skill, 26))