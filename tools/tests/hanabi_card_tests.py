#sys.path.append("../")
import unittest
from tools.hanabi_card import HanabiCard, HanabiColor

class HanabiCardTests(unittest.TestCase):
    def setUp(self):
        self.unknown_card = HanabiCard(HanabiColor.RED, 5)
        self.known_card = HanabiCard(HanabiColor.BLUE, 1)
        self.known_card.disclose_color()
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

if __name__ == '__main__':
    unittest.main()