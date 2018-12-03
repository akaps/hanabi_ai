import unittest
import hanabi_ai.players.player_utils as utils
import hanabi_ai.model.hanabi_moves as moves
from hanabi_ai.model.hanabi_game_info import GameInfo

class PlayerUtilsTests(unittest.TestCase):
    def setUp(self):
        self.info_player_0 = GameInfo()
        self.info_player_0.hands = [['??', '??'], ['R1', 'W3']]
        self.info_player_0.known_info = [['??', '??'], ['??', '??']]
        self.info_player_0.scored_cards = {
            'R' : 0
        }
        self.info_player_0.disclosures = 4
        self.info_player_0.num_players = 2

    def test_discard_oldest_can_discard(self):
        actual = utils.discard_oldest_first(1, self.info_player_0)
        self.assertIsInstance(actual, moves.HanabiDiscardAction)
        self.assertEqual(1, actual.player_id)
        self.assertEqual(0, actual.card)

    def test_discard_oldest_cannot(self):
        self.info_player_0.disclosures = 8
        self.assertIsNone(utils.discard_oldest_first(0, self.info_player_0))

    def test_play_safe_card_can_play(self):
        self.info_player_0.known_info[0][1] = 'R1'
        actual = utils.play_safe_card(0, self.info_player_0)
        self.assertIsInstance(actual, moves.HanabiPlayAction)
        self.assertEqual(0, actual.player_id)
        self.assertEqual(1, actual.card)

    def test_play_safe_card_cannot_play(self):
        self.assertIsNone(utils.play_safe_card(0, self.info_player_0))

    def test_tell_randomly_cannot_tell(self):
        self.info_player_0.disclosures = 0
        self.assertIsNone(utils.tell_randomly(0, self.info_player_0, 12))

    def test_tell_randomly_color(self):
        actual = utils.tell_randomly(0, self.info_player_0, 12)
        self.assertIsInstance(actual, moves.HanabiDiscloseColorAction)
        self.assertEqual(0, actual.player_id)
        self.assertEqual(1, actual.to_whom)
        self.assertEqual('R', actual.color)

    def test_tell_randomly_rank(self):
        actual = utils.tell_randomly(0, self.info_player_0, 26)
        self.assertIsInstance(actual, moves.HanabiDiscloseRankAction)
        self.assertEqual(0, actual.player_id)
        self.assertEqual(1, actual.to_whom)
        self.assertEqual(3, actual.rank)

    def test_cannot_discard_randomly(self):
        self.info_player_0.disclosures = 8
        self.assertIsNone(utils.discard_randomly(0, self.info_player_0, 26))

    def test_discard_randomly(self):
        actual = utils.discard_randomly(0, self.info_player_0, 26)
        self.assertIsInstance(actual, moves.HanabiDiscardAction)
        self.assertEqual(0, actual.player_id)
        self.assertEqual(1, actual.card)
