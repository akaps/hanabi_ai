import unittest
from hanabi_ai.model.hanabi_hand import HanabiHand
from hanabi_ai.model.hanabi_card import HanabiCard, HanabiColor

class HanabiHandTests(unittest.TestCase):
    def setUp(self):
        self.hand = HanabiHand()
        self.hand.add(HanabiCard(HanabiColor.BLUE, 2))
        self.hand.add(HanabiCard(HanabiColor.GREEN, 5))
        self.hand.add(HanabiCard(HanabiColor.BLUE, 1))

    def test_hand_cardAt(self):
        self.assertEqual(self.hand.card_at(0), HanabiCard(HanabiColor.BLUE, 2))

    def test_hand_removeCardAt(self):
        card = self.hand.remove_card_at(0)
        self.assertEqual(card, HanabiCard(HanabiColor.BLUE, 2))

    def test_hand_addCard(self):
        self.hand.add(HanabiCard(HanabiColor.WHITE, 1))
        self.assertEqual(self.hand.card_at(2), HanabiCard(HanabiColor.BLUE, 1))

    def test_hand_knownCards(self):
        self.assertEqual(["??", "??", "??"], self.hand.show_cards(True))
        self.hand.disclose_rank(2)
        self.assertEqual(["?2", "??", "??"], self.hand.show_cards(True))
        self.hand.disclose_color(HanabiColor.BLUE)
        self.assertEqual(["B2", "??", "B?"], self.hand.show_cards(True))

    def test_hand_discloseColor(self):
        self.assertEqual(["??", "??", "??"], self.hand.show_cards(True))
        self.hand.disclose_color(HanabiColor.GREEN)
        self.assertEqual(["??", "G?", "??"], self.hand.show_cards(True))

    def test_hand_discloseRank(self):
        self.assertEqual(["??", "??", "??"], self.hand.show_cards(True))
        self.hand.disclose_rank(5)
        self.assertEqual(["??", "?5", "??"], self.hand.show_cards(True))

    def test_hand_with_rainbow_cards(self):
        card1 = HanabiCard(HanabiColor.RED, 2)
        card2 = HanabiCard(HanabiColor.RAINBOW, 2)
        hand = HanabiHand()
        hand.add(card1)
        hand.add(card2)
        self.assertEqual(["??", "??"], hand.show_cards(True))
        hand.disclose_color(HanabiColor.RED, True)
        self.assertEqual(["R?", "R?"], hand.show_cards(True))
        hand.disclose_color(HanabiColor.GREEN, True)
        self.assertEqual(["R?", "*?"], hand.show_cards(True))

if __name__ == '__main__':
    unittest.main()
