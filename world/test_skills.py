"""
Skills test module.
"""
from unittest import skip

from django.test import TestCase
from evennia.utils.test_resources import EvenniaTest
from typeclasses.characters import Character
from world.skills import load_skill, ALL_SKILLS, apply_skills, SkillException
from world.archetypes import PRIMARY_TRAITS


class LoadSkillTestCase(TestCase):
    """Test case for the `load_skill` module function."""
    def test_load_skill(self):
        for name in ALL_SKILLS:
            s = load_skill(name)
            self.assertEqual(s.name.lower(), name)
            self.assertIn(s.trait, PRIMARY_TRAITS)

class ApplySkillsTestCase(EvenniaTest):
    character_typeclass = Character

    def test_apply_skills(self):
        skills = {
            'dodge': 1,
            'rifles': 0,
            'powered armor': 10,
            'piloting': 0,
        }
        apply_skills(self.char1, skills)
        for k, v in skills.iteritems():
            self.assertEqual(v, self.char1.skills[k])

        self.assertRaises(SkillException, apply_skills,
                          self.char1, {"notaskill": 1})
