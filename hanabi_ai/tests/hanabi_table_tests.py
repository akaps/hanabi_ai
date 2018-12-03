import unittest
from hanabi_ai.model.hanabi_table import HanabiTable
from hanabi_ai.model.hanabi_card import HanabiColor
from hanabi_ai.model.hanabi_deck import HanabiVariant

def diagnose(table):
    print('Player 0')
    print(table.info_for_player(1).hands[0])
    print('Player 1')
    print(table.info_for_player(0).hands[1])
    print(str(table))
    print(table.scored_cards)

class HanabiTableTests(unittest.TestCase):
    def setUp(self):
        self.table = HanabiTable(2, 1, HanabiVariant.basic)

    def test_table_play_card(self):
        self.assertFalse(self.table.is_game_over())
        self.assertEqual(len(self.table.deck), 40)
        self.table.play_card(0, 0)
        self.assertFalse(self.table.is_game_over())
        self.assertEqual(len(self.table.deck), 39)

    def test_table_discard_card(self):
        self.assertFalse(self.table.is_game_over())
        self.assertEqual(len(self.table.deck), 40)
        self.assertEqual(len(self.table.discard), 0)
        self.table.discard_card(0, 0)
        self.assertFalse(self.table.is_game_over())
        self.assertEqual(len(self.table.deck), 39)
        self.assertEqual(len(self.table.discard), 1)

    def test_table_disclose_color(self):
        self.assertEqual(["??", "??", "??", "??", "??"], self.table.info_for_player(0).hands[0])
        self.table.disclose_color(0, 0, HanabiColor.RED)
        self.assertEqual(["R?", "??", "R?", "??", "??"], self.table.info_for_player(0).hands[0])

    def test_table_disclose_rank(self):
        self.assertEqual(["??", "??", "??", "??", "??"], self.table.info_for_player(0).hands[0])
        self.table.disclose_rank(0, 0, 3)
        self.assertEqual(["??", "??", "??", "??", "?3"], self.table.info_for_player(0).hands[0])

    def test_table_game_over_mistakes(self):
        self.assertFalse(self.table.is_game_over())

        self.table.play_card(0, 1)
        self.assertFalse(self.table.is_game_over())
        self.assertEqual(self.table.mistakes_left, 2)

        self.table.play_card(1, 0)
        self.assertFalse(self.table.is_game_over())
        self.assertEqual(self.table.mistakes_left, 1)

        self.table.play_card(1, 0)
        self.assertTrue(self.table.is_game_over())
        self.assertEqual(self.table.mistakes_left, 0)

    def test_game_over_no_more_cards(self):
        self.assertFalse(self.table.is_game_over())
        for i in range(0, 42):
            self.assertEqual(len(self.table.discard), i)
            self.assertFalse(self.table.is_game_over())
            self.table.discard_card(0, 0)
        self.assertTrue(self.table.is_game_over())

    def test_game_over_and_won(self):
        self.table.play_card(1, 2)
        self.assertEquals(1, self.table.score())
        self.table.play_card(0, 0)
        self.assertEquals(2, self.table.score())
        self.table.play_card(0, 4)
        self.assertEquals(3, self.table.score())
        self.table.scored_cards[HanabiColor.RED] = 5
        self.table.scored_cards[HanabiColor.BLUE] = 5
        self.table.scored_cards[HanabiColor.GREEN] = 5
        self.table.scored_cards[HanabiColor.YELLOW] = 5
        self.table.scored_cards[HanabiColor.WHITE] = 5
        self.assertEquals(25, self.table.score())
        self.assertTrue(self.table.is_game_over())

    def test_table_str(self):
        self.assertEqual('Score: 0, '
                         'Cards remaining: 40, '
                         'Discarded: 0, '
                         'Disclosures left: 8, '
                         'Mistakes left: 3',
                         str(self.table))
        self.table.play_card(1, 0)
        self.assertEqual('Score: 0, '
                         'Cards remaining: 39, '
                         'Discarded: 1, '
                         'Disclosures left: 8, '
                         'Mistakes left: 2',
                         str(self.table))
        self.table.disclose_color(0, 0, HanabiColor.RED)
        self.assertEqual('Score: 0, '
                         'Cards remaining: 39, '
                         'Discarded: 1, '
                         'Disclosures left: 7, '
                         'Mistakes left: 2',
                         str(self.table))
        self.table.discard_card(0, 0)
        self.assertEqual('Score: 0, '
                         'Cards remaining: 38, '
                         'Discarded: 2, '
                         'Disclosures left: 8, '
                         'Mistakes left: 2',
                         str(self.table))

    def test_table_info_for_player(self):
        info = self.table.info_for_player(0)
        self.assertEqual(info.score, 0)
        self.assertEqual(info.deck_size, 40)
        self.assertEqual(len(info.discarded), 0)
        self.assertEqual(info.disclosures, 8)
        self.assertEqual(info.mistakes_left, 3)
        self.assertEqual(info.num_players, 2)
        self.assertEqual(info.hands[0], ["??", "??", "??", "??", "??"])
        self.assertEqual(info.hands[1], ["W4", "Y5", "B1", "G5", "W1"])
        self.assertEqual(info.known_info[0], ["??", "??", "??", "??", "??"])
        self.assertEqual(info.known_info[1], ["??", "??", "??", "??", "??"])
        self.assertEqual(info.scored_cards["R"], 0)
        self.assertEqual(info.scored_cards["B"], 0)
        self.assertEqual(info.scored_cards["G"], 0)
        self.assertEqual(info.scored_cards["Y"], 0)
        self.assertEqual(info.scored_cards["W"], 0)
        self.assertTrue("*" not in info.scored_cards)

    def test_table_score(self):
        self.assertEqual(0, self.table.score())

    def test_play_5_get_disclosure(self):
        self.play_to_white_5()
        self.table.disclose_rank(0, 0, 0)
        self.assertEquals(7, self.table.disclosures)
        self.table.play_card(0, 0)
        self.assertEqual(8, self.table.disclosures)

    def test_play_5_no_extra_disclosure(self):
        self.play_to_white_5()
        self.assertEquals(8, self.table.disclosures)
        self.table.play_card(0, 0)
        self.assertEqual(8, self.table.disclosures)

    def play_to_white_5(self):
        self.table.play_card(0, 0)
        self.table.play_card(1, 2)
        self.table.play_card(1, 4)
        self.table.play_card(1, 0)
        self.table.discard_card(0, 3)
        self.assertEquals(8, self.table.disclosures)
        self.table.discard_card(0, 3)
        self.table.discard_card(1, 1)
        self.table.play_card(0, 4)
        self.table.play_card(0, 3)
        self.table.play_card(0, 4)
        self.table.play_card(1, 4)
        self.table.play_card(1, 0)

if __name__ == '__main__':
    unittest.main()
