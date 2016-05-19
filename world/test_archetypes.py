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

    def test_valid_allocations(self):
        archetypes.apply_archetype(self.char1, 'soldier', reset=True)
        self.assertTrue(archetypes.validate_primary_traits(self.char1.traits))

    @skip("Test after confirm above")
    def test_get_remaining(self):
        """confirm function of `get_remaning_allocation`"""
        self.assertEqual(
            archetypes.get_remaining_allocation(self.char1.traits), 8)
        # do allocations
        self.char1.traits.STR.base += 2
        self.char1.traits.PER.base += 1
        self.char1.traits.INT.base += 1
        self.char1.traits.DEX.base += 1
        self.char1.traits.CHA.base += 1
        self.char1.traits.VIT.base += 2
        # confirm zero points left
        self.assertEqual(
            archetypes.get_remaining_allocation(self.char1.traits), 0)

    @skip("Test after confirm above")
    def test_toomany_points(self):
        """confirm validation of over-allocated traits"""
        # perfect char not allowed
        for t in archetypes.PRIMARY_TRAITS:
            self.char1.traits[t].base = 10
        is_valid, errmsg = archetypes.validate_primary_traits(self.char1.traits)
        self.assertFalse(is_valid)
        self.assertEqual(errmsg, 'Too many trait points allocated.')
        # no more than 30 allowed
        archetypes.apply_archetype(self.char1, 'warrior', reset=True)
        self.char1.traits.INT.base += 9
        is_valid, errmsg = archetypes.validate_primary_traits(self.char1.traits)
        self.assertFalse(is_valid)
        self.assertEqual(errmsg, 'Too many trait points allocated.')

    @skip("Test after confirm above")
    def test_toofew_points(self):
        """confirm validation of under-allocated traits"""
        # fails before any allocations happen
        is_valid, errmsg = archetypes.validate_primary_traits(self.char1.traits)
        self.assertFalse(is_valid)
        self.assertEqual(errmsg, 'Not enough trait points allocated.')
        # no less than 30 allowed
        self.char1.traits.INT.base += 6
        is_valid, errmsg = archetypes.validate_primary_traits(self.char1.traits)
        self.assertFalse(is_valid)
        self.assertEqual(errmsg, 'Not enough trait points allocated.')

    @skip("Test after confirm above")
    def test_calculate_secondary_traits(self):
        """confirm functionality of `calculate_secondary_traits` function"""
        self.char1.traits.STR.base += 3
        self.char1.traits.DEX.base += 2
        self.char1.traits.VIT.base += 3
        archetypes.calculate_secondary_traits(self.char1.traits)
        self.assertEqual(self.char1.traits.HP.actual, 9)
        self.assertEqual(self.char1.traits.SP.actual, 9)
        self.assertEqual(self.char1.traits.BM.actual, 0)
        self.assertEqual(self.char1.traits.WM.actual, 0)
        self.assertEqual(self.char1.traits.BM.max, 0)
        self.assertEqual(self.char1.traits.WM.max, 0)
        self.assertEqual(self.char1.traits.FORT.actual, 9)
        self.assertEqual(self.char1.traits.REFL.actual, 4)
        self.assertEqual(self.char1.traits.WILL.actual, 1)
        self.assertEqual(self.char1.traits.ATKM.actual, 9)
        self.assertEqual(self.char1.traits.ATKR.actual, 1)
        self.assertEqual(self.char1.traits.ATKU.actual, 6)
        self.assertEqual(self.char1.traits.DEF.actual, 6)
        self.assertEqual(self.char1.traits.ENC.max, 180)
        # if any allocated to MAG, WM and BM have max=10
        self.char1.traits.STR.base -= 1
        self.char1.traits.MAG.base += 1
        archetypes.calculate_secondary_traits(self.char1.traits)
        self.assertEqual(self.char1.traits.BM.max, 10)
        self.assertEqual(self.char1.traits.WM.max, 10)

    def test_load_archetype(self):
        for k, v in self.at_data.iteritems():
            a = archetypes.load_archetype(k)
            self.assertIsInstance(a, archetypes.Archetype)


