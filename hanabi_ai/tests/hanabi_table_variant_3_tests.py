import unittest
from hanabi_ai.model.hanabi_table import HanabiTable
from hanabi_ai.model.hanabi_card import HanabiColor
from hanabi_ai.model.hanabi_deck import HanabiVariant

class HanabiTableVariant3Tests(unittest.TestCase):
    def setUp(self):
        self.table = HanabiTable(2, 9, HanabiVariant.rainbow_wild)

    def test_play_correct_rainbow(self):
        for _ in range(0, 5):
            self.table.discard_card(0, 0)
        self.table.play_card(0, 2)
        self.assertEqual(1, self.table.score())
        self.assertEqual(1, self.table.info_for_player(0).scored_cards["*"])

    def test_play_incorrect_rainbow(self):
        self.table.play_card(0, 2)
        self.table.play_card(1, 4)
        self.assertEqual(1, self.table.score())
        self.assertEqual(1, self.table.info_for_player(0).scored_cards["W"])
        self.assertEqual(2, self.table.mistakes_left)

    def test_table_disclose_color(self):
        self.table.disclose_color(0, 1, HanabiColor.WHITE)
        self.assertEqual(["W?", "W?", "??", "??", "W?"], self.table.info_for_player(1).hands[1])
        self.table.disclose_color(0, 1, HanabiColor.RED)
        self.assertEqual(["*?", "W?", "??", "R?", "*?"], self.table.info_for_player(1).hands[1])

    def test_cannot_disclose_rainbow(self):
        self.assertFalse(self.table.can_disclose_color(HanabiColor.RAINBOW))
        self.assertTrue(self.table.can_disclose_color(HanabiColor.RED))

if __name__ == '__main__':
    unittest.main()
