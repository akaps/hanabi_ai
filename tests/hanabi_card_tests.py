#sys.path.append("../")
import unittest
from hanabi_ai.model.hanabi_card import HanabiCard, HanabiColor

class HanabiCardTests(unittest.TestCase):
    def setUp(self):
        self.unknown_card = HanabiCard(HanabiColor.RED, 5)
        self.known_card = HanabiCard(HanabiColor.BLUE, 1)
        self.known_card.disclose_color(HanabiColor.BLUE)
        self.known_card.disclose_rank()
        self.rank_known_card = HanabiCard(HanabiColor.GREEN, 3)
        self.rank_known_card.disclose_rank()

    def test_unknown_card_color(self):
        self.assertEqual(self.unknown_card.color, HanabiColor.RED)

    def test_known_card_color(self):
        self.assertEqual(self.known_card.color, HanabiColor.BLUE)

    def test_rank_known_card_color(self):
        self.assertEqual(self.rank_known_card.color, HanabiColor.GREEN)

    def test_unknow_card_rank(self):
        self.assertEqual(self.unknown_card.rank, 5)

    def test_known_card_rank(self):
        self.assertEqual(self.known_card.rank, 1)

    def test_rank_known_card_rank(self):
        self.assertEqual(self.rank_known_card.rank, 3)

    def test_unknown_card_str(self):
        self.assertEqual(str(self.unknown_card), "R5")

    def test_known_card_str(self):
        self.assertEqual(str(self.known_card), "B1")

    def test_rank_known_card_str(self):
        self.assertEqual(str(self.rank_known_card), "G3")

    def test_unknown_card_known(self):
        self.assertEqual(self.unknown_card.known(), "??")

    def test_known_card_known(self):
        self.assertEqual(self.known_card.known(), "B1")

    def test_rank_known_card_known(self):
        self.assertEqual(self.rank_known_card.known(), "?3")

    def test_eq(self):
        self.assertEqual(self.rank_known_card, HanabiCard(HanabiColor.GREEN, 3))

    def test_ne(self):
        self.assertNotEqual(self.known_card, self.rank_known_card)

    def test_rainbow_card(self):
        rainbow_card = HanabiCard(HanabiColor.RAINBOW, 2)
        self.assertEqual("*2", str(rainbow_card))
        self.assertEqual("??", rainbow_card.known())
        rainbow_card.disclose_rank()
        self.assertEqual("?2", rainbow_card.known())
        rainbow_card.disclose_color(HanabiColor.RED, True)
        self.assertEqual("R2", rainbow_card.known())
        rainbow_card.disclose_color(HanabiColor.GREEN, True)
        self.assertEqual("*2", rainbow_card.known())

    def test_rainbow_card_avoid_accidental_reveal(self):
        rainbow_card = HanabiCard(HanabiColor.RAINBOW, 2)
        self.assertEqual("??", rainbow_card.known())
        rainbow_card.disclose_color(HanabiColor.RED, True)
        self.assertEqual("R?", rainbow_card.known())
        rainbow_card.disclose_color(HanabiColor.RED, True)
        self.assertEqual("R?", rainbow_card.known())

if __name__ == '__main__':
    unittest.main()
