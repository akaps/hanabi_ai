import unittest
from hanabi_ai.model.table import HanabiTable
from hanabi_ai.model.card import HanabiCard, HanabiColor
from hanabi_ai.model.deck import HanabiVariant

class HanabiTableVariant1Tests(unittest.TestCase):
    def setUp(self):
        self.table = HanabiTable(2, 1, HanabiVariant.sixth_suit)

    def test_play_correct_rainbow(self):
        self.table.play_card(0, 0)
        self.assertEqual(1, self.table.score())

    def test_play_incorrect_rainbow(self):
        self.table.discard_card(0, 0)
        self.table.discard_card(0, 0)
        self.table.discard_card(0, 4)
        self.table.discard_card(0, 0)
        self.table.discard_card(0, 1)
        #play yellow 1 and 2
        self.table.play_card(0, 3)
        self.assertEqual(1, self.table.score())
        self.table.play_card(0, 2)
        self.assertEqual(2, self.table.score())
        #play rainbow 3, cannot since it is not wild
        self.table.play_card(0, 0)
        self.assertEqual(2, self.table.score())
        self.assertEqual(2, self.table.mistakes_left)
        self.assertTrue(HanabiCard(HanabiColor.RAINBOW, 3) in self.table.discard.discarded())

    def test_table_disclose_color(self):
        self.assertEqual(["??", "??", "??", "??", "??"], self.table.info_for_player(0).hands[0])
        self.table.disclose_color(0, 0, HanabiColor.RAINBOW)
        self.assertEqual(["*?", "??", "*?", "*?", "??"], self.table.info_for_player(0).hands[0])

    def test_table_info_for_player(self):
        info = self.table.info_for_player(0)
        self.assertEqual(info.deck_size, 50)

    def test_can_disclose_color(self):
        self.assertTrue(self.table.can_disclose_color('R'))
        self.assertTrue(self.table.can_disclose_color('G'))
        self.assertTrue(self.table.can_disclose_color('B'))
        self.assertTrue(self.table.can_disclose_color('W'))
        self.assertTrue(self.table.can_disclose_color('Y'))
        self.assertTrue(self.table.can_disclose_color('*'))
        self.assertFalse(self.table.can_disclose_color('A'))

    def test_table_with_rainbow_deck(self):
        #play a rainbow onto its own pile
        self.table.play_card(0, 0)
        self.assertEqual(1, self.table.score())
        #play a rainbow at the wrong time
        self.table.play_card(0, 2)
        self.assertEqual(1, self.table.score())
        self.assertEqual(1, len(self.table.discard))
        #confirm that we are adding to the rainbow pile
        self.assertEqual(1, self.table.info_for_player(0).scored_cards["*"])

if __name__ == '__main__':
    unittest.main()
