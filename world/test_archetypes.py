"""
Unit tests for world.archetypes module.
"""

from unittest import skip

from world import archetypes
from typeclasses.characters import Character
from evennia.utils.test_resources import EvenniaTest


class ArchetypeTestCase(EvenniaTest):
    """Test case for Archetype classes."""
    character_typeclass = Character

    def test_init(self):
        for k, v in archetypes.ARCHETYPE_DATA.iteritems():
            a = archetypes.Archetype(v)
            self.assertIsInstance(a, archetypes.Archetype, msg="Invalid %s" % k)

        bad_data = archetypes.ARCHETYPE_DATA['soldier'].copy()
        del bad_data["name"]
        self.assertRaises(archetypes.ArchetypeException, archetypes.Archetype, bad_data)

    def test_ldesc(self):
        for k, v in archetypes.ARCHETYPE_DATA.iteritems():
            a = archetypes.Archetype(v)
            self.assertTrue(a.ldesc)

    def test_desc(self):
        for k, v in archetypes.ARCHETYPE_DATA.iteritems():
            a = archetypes.Archetype(v)
            self.assertTrue(a.desc)


class PublicFunctionsTestCase(EvenniaTest):
    """Test case for the supporting module functions."""
    character_typeclass = Character

    def setUp(self):
        super(PublicFunctionsTestCase, self).setUp()
        self.at_data = archetypes.ARCHETYPE_DATA.copy()

    def test_apply_archetype(self):
        data = self.at_data.copy()
        for k, v in data.iteritems():
            if self.char1.db.archetype is not None:
                archetypes.apply_archetype(self.char1, k, reset=True)
            else:
                archetypes.apply_archetype(self.char1, k)
            self.assertEqual(self.char1.traits.AGL, data[k]['AGL'])
            self.assertEqual(self.char1.traits.STR, data[k]['STR'])
            self.assertEqual(self.char1.traits.KNW, data[k]['KNW'])
            self.assertEqual(self.char1.traits.MCH, data[k]['MCH'])
            self.assertEqual(self.char1.traits.PER, data[k]['PER'])
            self.assertEqual(self.char1.traits.TCH, data[k]['TCH'])
            self.assertEqual(self.char1.traits.WOUNDS, 0)
            self.assertEqual(self.char1.traits.FATE, 0)
            self.assertEqual(self.char1.traits.CP, 0)
            self.assertEqual(self.char1.traits.ENC, 0)

    def test_get_remaining_allocation(self):
        """confirm function of `get_remaning_allocation`"""
        for k in self.at_data:
            archetypes.apply_archetype(self.char1, k, reset=True)
            self.assertEqual(
                archetypes.get_remaining_allocation(self.char1.traits), 0)
            # do allocations
            self.char1.traits.AGL.base += -2
            self.char1.traits.STR.base += -1
            self.char1.traits.KNW.base += -1
            self.char1.traits.MCH.base += -1
            self.char1.traits.PER.base += -1
            self.char1.traits.TCH.base += -2
            # confirm zero points left
            self.assertEqual(
                archetypes.get_remaining_allocation(self.char1.traits), 8)

    def test_valid_primary_points(self):
        # This has side benefit of testing all the archtypes to make sure they have enough points.
        for k in self.at_data:
            archetypes.apply_archetype(self.char1, k, reset=True)
        self.assertTrue(archetypes.validate_primary_traits(self.char1.traits))

    def test_finalize_traits(self):
        for k in self.at_data:
            archetypes.apply_archetype(self.char1, k, reset=True)
            original = self.char1.traits.STR.base
            self.char1.traits.STR.mod += 3
            archetypes.finalize_traits(self.char1.traits)
            self.assertEqual(self.char1.traits.STR, original + 3)

    def test_load_archetype(self):
        for k, v in self.at_data.iteritems():
            a = archetypes.load_archetype(k)
            self.assertIsInstance(a, archetypes.Archetype)


