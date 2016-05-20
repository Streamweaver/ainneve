from evennia.utils.test_resources import EvenniaTest

from typeclasses.characters import Character
from world import economy

class TransferTestCase(EvenniaTest):
    character_typeclass = Character

    def test_transfer_funds(self):
        # Test no funds
        self.assertRaises(economy.InsufficientFunds,
                          economy.transfer_funds,
                          self.char1,
                          self.char2,
                          1)

        self.char1.db.credits = 100

        # Test xfer too much
        self.assertRaises(economy.InsufficientFunds,
                          economy.transfer_funds,
                          self.char1,
                          self.char2,
                          1000)

        for i in range(1, 11):
            economy.transfer_funds(self.char1, self.char2, 10)
            self.assertEqual(self.char1.db.credits, 100 - i*10)
            self.assertEqual(self.char2.db.credits, i*10)

        # Give 1000 credits to char1 and make sure they named it.
        economy.transfer_funds(None, self.char1, 1000)
        self.assertEqual(self.char1.db.credits, 1000)

        # Take 50 from char2 to nowhere.
        economy.transfer_funds(self.char2, None, 50)
        self.assertEqual(self.char2.db.credits, 50)

        # char1 should still have same as before.
        self.assertEqual(self.char1.db.credits, 1000)

class FormatCreditsTestCase(EvenniaTest):
    character_typeclass = Character

    def test_format_credits(self):
        data = (
            (10, "|w10|n cr."),
            (1000, "|w1,000|n cr."),
            (10000, "|w10,000|n cr."),
            (100000, "|w100,000|n cr."),
            (1000000, "|w1,000,000|n cr.")
        )
        for credits, exp in data:
            self.assertEqual(economy.format_credits(credits), exp)