"""
Skills test module.
"""
from unittest import skip

from django.test import TestCase
from evennia.utils.test_resources import EvenniaTest
from typeclasses.characters import Character
from world.skills import load_skill, ALL_SKILLS
from world.archetypes import PRIMARY_TRAITS


class LoadSkillTestCase(TestCase):
    """Test case for the `load_skill` module function."""
    def test_load_skill(self):
        print(ALL_SKILLS)
        for name in ALL_SKILLS:
            s = load_skill(name)
            self.assertEqual(s.name.lower(), name)
            self.assertIn(s.base, PRIMARY_TRAITS)

@skip("Skip until archtypes are refactored")
class CharSkillsTestCase(EvenniaTest):
    """Test case for module functions that operate on characters."""
    def setUp(self):
        self.character_typeclass = Character
        super(CharSkillsTestCase, self).setUp()
        archetypes.apply_archetype(self.char1, 'warrior')
        tr = self.char1.traits
        tr.STR.base += 2
        tr.PER.base += 1
        tr.INT.base += 1
        tr.DEX.base += 1
        tr.CHA.base += 1
        tr.VIT.base += 2

    def test_apply_skills(self):
        """test module function `apply_skills`"""
        skills.apply_skills(self.char1)
        sk = self.char1.skills
        self.assertEqual(sk.escape.actual, 8)
        self.assertEqual(sk.climb.actual, 8)
        self.assertEqual(sk.jump.actual, 8)
        self.assertEqual(sk.lockpick.actual, 2)
        self.assertEqual(sk.listen.actual, 2)
        self.assertEqual(sk.sense.actual, 2)
        self.assertEqual(sk.appraise.actual, 2)
        self.assertEqual(sk.medicine.actual, 2)
        self.assertEqual(sk.survival.actual, 2)
        self.assertEqual(sk.balance.actual, 5)
        self.assertEqual(sk.sneak.actual, 5)
        self.assertEqual(sk.throwing.actual, 5)
        self.assertEqual(sk.animal.actual, 5)
        self.assertEqual(sk.barter.actual, 5)
        self.assertEqual(sk.leadership.actual, 5)

    def test_validate_skills(self):
        """test module function `apply_skills`"""
        skills.apply_skills(self.char1)
        # not
        self.assertFalse(skills.validate_skills(self.char1)[0])
        self.assertIn('Not enough -1',
                      skills.validate_skills(self.char1)[1])
        sk = self.char1.skills
        sk.escape.minus += 1
        sk.climb.minus += 1
        sk.jump.minus += 1
        sk.medicine.plus += 1
        self.assertTrue(skills.validate_skills(self.char1)[0])
        sk.appraise.plus += 1
        self.assertFalse(skills.validate_skills(self.char1)[0])
        self.assertIn('Not enough +1',
                      skills.validate_skills(self.char1)[1])

    def test_finalize_skills(self):
        """test module function `finalize_skills`"""
        skills.apply_skills(self.char1)
        # allocate skills for char1
        sk = self.char1.skills
        sk.escape.minus += 1
        sk.climb.minus += 1
        sk.jump.minus += 1
        sk.medicine.plus += 1
        skills.finalize_skills(sk)
        # confirm the plusses and minuses are applied
        self.assertEqual(sk.escape.actual, 7)
        self.assertEqual(sk.climb.actual, 7)
        self.assertEqual(sk.jump.actual, 7)
        self.assertEqual(sk.medicine.actual, 3)
        # confirm plus/minus counters are deleted
        with self.assertRaises(AttributeError):
            x = sk.escape.plus
        with self.assertRaises(AttributeError):
            x = sk.escape.minus
