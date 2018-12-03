import unittest
from hanabi_ai.model.discard_pile import HanabiDiscard
from hanabi_ai.model.card import HanabiCard, HanabiColor

class HanabiDiscardTests(unittest.TestCase):

    def setUp(self):
        self.discard = HanabiDiscard()
        self.to_discard = HanabiCard(HanabiColor.RED, 3)

    def test_discard_add(self):
        self.assertEqual([], self.discard.discarded())
        self.discard.add(self.to_discard)
        self.assertEqual([self.to_discard], self.discard.discarded())
        self.discard.add(self.to_discard)
        self.assertEqual([self.to_discard, self.to_discard], self.discard.discarded())

    def test_discard_contains(self):
        self.assertFalse(self.discard.contains(self.to_discard))
        self.discard.add(self.to_discard)
        self.assertTrue(self.discard.contains(self.to_discard))

    def test_discard_str(self):
        self.assertEqual("", str(self.discard))
        self.discard.add(self.to_discard)
        self.assertEqual("R3", str(self.discard))
        self.discard.add(self.to_discard)
        self.assertEqual("R3 R3", str(self.discard))

if __name__ == '__main__':
    unittest.main()
