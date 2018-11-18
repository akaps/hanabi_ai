import unittest
from hanabi_ai.model.hanabi_table import HanabiTable
from hanabi_ai.model.hanabi_hand import HanabiHand
from hanabi_ai.model.hanabi_card import HanabiCard, HanabiColor
from tests.hanabi_table_tests import diagnose
from hanabi_ai.model.hanabi_deck import HanabiVariant

class HanabiTableVariant2Tests(unittest.TestCase):
    def setUp(self):
        self.table = HanabiTable(2, 1, HanabiVariant.sixth_suit_hard)

    def test_table_play_card_correct_rainbow(self):
        #white 1
        self.table.play_card(0,2)
        self.table.discard_card(0,0)
        self.table.discard_card(0,0)
        self.table.discard_card(0,0)
        #play rainbow 1, 2
        self.table.play_card(0,4)
        self.table.play_card(0,0)
        self.assertEqual(3, self.table.score())

    def test_table_play_card_incorrect_rainbow(self):
        #play white 1
        self.table.play_card(0,2)
        self.assertEqual(1, self.table.score())
        #play rainbow 2, cannot since it is not wild
        self.table.play_card(0,3)
        self.assertEqual(1, self.table.score())
        self.assertEqual(2, self.table.mistakes_left)
        self.assertTrue(HanabiCard(HanabiColor.RAINBOW, 2) in self.table.discard.discarded())

    def test_table_disclose_color(self):
        self.assertEqual(["??", "??", "??", "??", "??"], self.table.info_for_player(0).hands[0])
        self.table.disclose_color(0, 0, HanabiColor.RAINBOW)
        self.assertEqual(["??", "??", "??", "??", "*?"], self.table.info_for_player(0).hands[0])

    def test_table_info_for_player(self):
        info = self.table.info_for_player(1)
        self.assertEqual(info.score, 0)
        self.assertEqual(info.deck_size, 45)
        self.assertEqual(len(info.discarded), 0)
        self.assertEqual(info.disclosures, 8)
        self.assertEqual(info.mistakes_left, 3)
        self.assertEqual(info.num_players, 2)
        self.assertEqual(info.hands[0], ["Y4", "B3", "W1", "G3", "*2"])
        self.assertEqual(info.hands[1], ["??", "??", "??", "??", "??"])
        self.assertEqual(info.known_info[0], ["??", "??", "??", "??", "??"])
        self.assertEqual(info.known_info[1], ["??", "??", "??", "??", "??"])
        self.assertEqual(info.scored_cards["R"], 0)
        self.assertEqual(info.scored_cards["B"], 0)
        self.assertEqual(info.scored_cards["G"], 0)
        self.assertEqual(info.scored_cards["Y"], 0)
        self.assertEqual(info.scored_cards["W"], 0)
        self.assertEqual(info.scored_cards["*"], 0)

if __name__ == '__main__':
    unittest.main()
