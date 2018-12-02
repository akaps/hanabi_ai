import unittest
from hanabi_ai.model.hanabi_deck import HanabiDeck

class HanabiDeckTests(unittest.TestCase):
    def setUp(self):
        self.simple_deck = HanabiDeck(1, False)
        self.rainbow_deck = HanabiDeck(1, True)

    def test_simple_deck_is_empty(self):
        self.assertFalse(self.simple_deck.is_empty())
        for _ in range(0, 50):
            self.simple_deck.draw_card()
        self.assertTrue(self.simple_deck.is_empty())

    def test_rainbow_deck_is_empty(self):
        self.assertFalse(self.rainbow_deck.is_empty())
        for _ in range(0, 60):
            self.rainbow_deck.draw_card()
        self.assertTrue(self.rainbow_deck.is_empty())

    def test_simple_deck_draw_card(self):
        card = self.simple_deck.draw_card()
        self.assertIsNotNone(card)
        self.assertEqual(49, len(self.simple_deck))

    def test_rainbow_deck_draw_card(self):
        card = self.rainbow_deck.draw_card()
        self.assertIsNotNone(card)
        self.assertEqual(59, len(self.rainbow_deck))

    def test_simple_deck_size(self):
        for i in range(50, 0):
            self.assertEqual(len(self.simple_deck), i)

    def test_rainbow_deck_size(self):
        for i in range(60, 0):
            self.assertEqual(len(self.simple_deck), i)

    def test_simple_deck_str(self):
        self.assertEqual("Cards remaining: 50", str(self.simple_deck))
        self.simple_deck.draw_card()
        self.assertEqual("Cards remaining: 49", str(self.simple_deck))

    def test_rainbow_deck_str(self):
        self.assertEqual("Cards remaining: 60", str(self.rainbow_deck))
        self.rainbow_deck.draw_card()
        self.assertEqual("Cards remaining: 59", str(self.rainbow_deck))

if __name__ == '__main__':
    unittest.main()
