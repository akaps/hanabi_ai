import unittest
from tools.hanabi_table import HanabiTable
from tools.hanabi_hand import HanabiHand
from tools.hanabi_card import HanabiCard, HanabiColor
from hanabi_table_tests import diagnose

class HanabiTableVariant3Tests(unittest.TestCase):
    def setUp(self):
        self.table = HanabiTable(2, 1, 3)

    def test_table_play_card_correct_rainbow(self):
        self.table.play_card(0,0) #*1
        self.assertEqual(1, self.table.score())
        self.assertEqual(1, self.table.info_for_player(0)["scored_cards"]["*"])

    def test_table_play_card_incorrect_rainbow(self):
        self.table.discard_card(0,0)
        self.table.discard_card(0,0)
        self.table.play_card(0,4) #W1
        self.table.discard_card(0,0)
        self.table.discard_card(1,0)
        self.table.discard_card(1,0)
        self.table.discard_card(1,0)
        self.table.discard_card(1,0)
        self.table.play_card(1,4) #R1
        self.table.play_card(0,1) #R2
        self.table.play_card(0,0) #*3
        diagnose(self.table)
        self.assertEqual(3, self.table.score())
        self.assertEqual(1, self.table.info_for_player(0)["scored_cards"]["W"])
        self.assertEqual(2, self.table.info_for_player(0)["scored_cards"]["R"])
        self.assertEqual(0, self.table.info_for_player(0)["scored_cards"]["*"])

    def test_table_disclose_color(self):
        self.table.disclose_color(0, HanabiColor.WHITE)
        self.assertEqual(["W?", "W?", "W?", "W?", "??"], self.table.info_for_player(0)["hands"][0])
        self.table.disclose_color(0, HanabiColor.RED)
        self.assertEqual(["*?", "W?", "*?", "*?", "R?"], self.table.info_for_player(0)["hands"][0])

    def test_table_disclose_color_cannot_choose_rainbow(self):
        self.assertFalse(self.table.can_disclose_color(HanabiColor.RAINBOW))
        self.assertTrue(self.table.can_disclose_color(HanabiColor.RED))

    def test_table_info_for_player(self):
        info = self.table.info_for_player(0)
        self.assertEqual(info["score"], 0)
        self.assertEqual(info["deck_size"], 50)
        self.assertEqual(len(info["discarded"]), 0)
        self.assertEqual(info["disclosures"], 8)
        self.assertEqual(info["mistakes_left"], 3)
        self.assertEqual(info["num_players"], 2)
        self.assertEqual(info["hands"][0], ["??", "??", "??", "??", "??"])
        self.assertEqual(info["hands"][1], ["B2", "*5", "Y3", "R3", "Y3"])
        self.assertEqual(info["known_info"][0], ["??", "??", "??", "??", "??"])
        self.assertEqual(info["known_info"][1], ["??", "??", "??", "??", "??"])
        self.assertEqual(info["scored_cards"]["R"], 0)
        self.assertEqual(info["scored_cards"]["B"], 0)
        self.assertEqual(info["scored_cards"]["G"], 0)
        self.assertEqual(info["scored_cards"]["Y"], 0)
        self.assertEqual(info["scored_cards"]["W"], 0)
        self.assertEqual(info["scored_cards"]["*"], 0)

if __name__ == '__main__':
    unittest.main()