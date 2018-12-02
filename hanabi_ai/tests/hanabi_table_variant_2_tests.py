import unittest
from hanabi_ai.model.hanabi_table import HanabiTable
from hanabi_ai.model.hanabi_card import HanabiCard, HanabiColor
from hanabi_ai.model.hanabi_deck import HanabiVariant

class HanabiTableVariant2Tests(unittest.TestCase):
    def setUp(self):
        self.table = HanabiTable(2, 6, HanabiVariant.sixth_suit_hard)

    def test_play_correct_rainbow(self):
        self.table.play_card(0, 1)
        self.table.play_card(1, 4)
        self.table.play_card(0, 4)
        self.assertEqual(3, self.table.score())

    def test_play_incorrect_rainbow(self):
        self.table.play_card(1, 4)
        self.table.play_card(1, 3)
        self.assertEqual(1, self.table.score())
        self.assertEqual(2, self.table.mistakes_left)
        self.assertTrue(HanabiCard(HanabiColor.RAINBOW, 3) in self.table.discard.discarded())

    def test_table_disclose_color(self):
        self.assertEqual(["??", "??", "??", "??", "??"], self.table.info_for_player(0).hands[0])
        self.table.disclose_color(0, 0, HanabiColor.GREEN)
        self.assertEqual(["??", "G?", "G?", "??", "??"], self.table.info_for_player(0).hands[0])

    def test_table_info_for_player(self):
        info = self.table.info_for_player(1)
        self.assertEqual(info.deck_size, 45)

if __name__ == '__main__':
    unittest.main()
