import unittest
from hanabi_ai.model.table import HanabiTable
from hanabi_ai.model.card import HanabiColor
from hanabi_ai.model.deck import HanabiVariant

class HanabiTableVariant3Tests(unittest.TestCase):
    def setUp(self):
        self.table = HanabiTable(2, 9, HanabiVariant.rainbow_wild)

    def test_play_correct_rainbow(self):
        self.table.play_card(0, 0) #*1
        self.assertEqual(1, self.table.score())
        self.assertEqual(1, self.table.info_for_player(0).scored_cards["*"])

    def test_play_incorrect_rainbow(self):
        self.table.play_card(0, 0)
        self.table.discard_card(0, 3)
        self.table.play_card(1, 0)
        self.table.play_card(1, 4)
        self.assertEqual(3, self.table.score())
        self.assertEqual(1, self.table.info_for_player(0).scored_cards["R"])
        self.assertEqual(1, self.table.info_for_player(0).scored_cards["G"])
        self.assertEqual(1, self.table.info_for_player(0).scored_cards["*"])

    def test_table_disclose_color(self):
        self.table.disclose_color(0, 0, HanabiColor.BLUE)
        self.assertEqual(["B?", "B?", "B?", "B?", "B?"], self.table.info_for_player(0).hands[0])
        self.table.disclose_color(0, 0, HanabiColor.RED)
        self.assertEqual(["*?", "B?", "B?", "B?", "*?"], self.table.info_for_player(0).hands[0])

    def test_cannot_disclose_rainbow(self):
        self.assertFalse(self.table.can_disclose_color(HanabiColor.RAINBOW))
        self.assertTrue(self.table.can_disclose_color(HanabiColor.RED))

if __name__ == '__main__':
    unittest.main()
