from unittest import TestCase

from .utils import d6str, d6roll

class UtilityTestCase(TestCase):
    """
    These should be short functions so using single class for now.
    """

    def test_d6str(self):
        data = [
            (3, "1D"), (4, "1D+1"), (5, "1D+2"),
            (6, "2D"), (7, "2D+1"), (8, "2D+2"),
            (9, "3D"), (10, "3D+1"), (11, "3D+2"),
        ]
        for value, exp in data:
            self.assertEqual(d6str(value), exp)

    def test_d6roll(self):
        for value in range(3, 16):
            for i in range(10000):
                min = value / 3 + value % 3
                max = value / 3 * 6 + value % 3
                roll = d6roll(value)
                self.assertTrue(min <= roll <= max, msg="{} is out or range for {}".format(roll, d6str(value)))
