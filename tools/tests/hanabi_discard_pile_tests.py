import unittest
from tools.hanabi_discard_pile import HanabiDiscard
from tools.hanabi_card import HanabiCard, HanabiColor

class HanabiDiscardTests(unittest.TestCase):

    def setUp(self):
        self.discard = HanabiDiscard()
        self.toDiscard = HanabiCard(HanabiColor.RED, 3)

    def test_discard_add(self):
        self.assertEqual([], self.discard.discarded())
        self.discard.add(self.toDiscard)
        self.assertEqual([self.toDiscard], self.discard.discarded())
        self.discard.add(self.toDiscard)
        self.assertEqual([self.toDiscard, self.toDiscard], self.discard.discarded())

    def test_discard_contains(self):
        self.assertFalse(self.discard.contains(self.toDiscard))
        self.discard.add(self.toDiscard)
        self.assertTrue(self.discard.contains(self.toDiscard))

    def test_discard_str(self):
        self.assertEqual("", str(self.discard))
        self.discard.add(self.toDiscard)
        self.assertEqual("R3", str(self.discard))
        self.discard.add(self.toDiscard)
        self.assertEqual("R3 R3", str(self.discard))

if __name__ == '__main__':
    unittest.main()