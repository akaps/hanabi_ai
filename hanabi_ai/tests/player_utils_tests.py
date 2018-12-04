import unittest
import hanabi_ai.players.utils as utils
import hanabi_ai.model.moves as moves
from hanabi_ai.model.game_info import GameInfo

class PlayerUtilsTests(unittest.TestCase):
    def setUp(self):
        self.info_player_0 = GameInfo()
        self.info_player_0.hands = [['??', '??'], ['R1', 'W3']]
        self.info_player_0.known_info = [['??', '??'], ['??', '??']]
        self.info_player_0.scored_cards = {
            'R' : 0,
            'W' : 0,
            'Y' : 0,
            'G' : 0,
            'B' : 0
        }
        self.info_player_0.disclosures = 4
        self.info_player_0.num_players = 2

    def test_discard_oldest_can_discard(self):
        res = utils.discard_oldest_first(1, self.info_player_0)
        self.assertIsInstance(res, moves.HanabiDiscardAction)
        self.assertEqual(1, res.player_id)
        self.assertEqual(0, res.card)

    def test_discard_oldest_cannot(self):
        self.info_player_0.disclosures = 8
        self.assertIsNone(utils.discard_oldest_first(0, self.info_player_0))

    def test_play_safe_card_can_play(self):
        self.info_player_0.known_info[0][1] = 'R1'
        res = utils.play_safe_card(0, self.info_player_0)
        self.assertIsInstance(res, moves.HanabiPlayAction)
        self.assertEqual(0, res.player_id)
        self.assertEqual(1, res.card)

    def test_play_safe_card_cannot_play(self):
        self.assertIsNone(utils.play_safe_card(0, self.info_player_0))

    def test_tell_randomly_cannot_tell(self):
        self.info_player_0.disclosures = 0
        self.assertIsNone(utils.tell_randomly(0, self.info_player_0, 12))

    def test_tell_randomly_color(self):
        res = utils.tell_randomly(0, self.info_player_0, 12)
        self.assertIsInstance(res, moves.HanabiDiscloseColorAction)
        self.assertEqual(0, res.player_id)
        self.assertEqual(1, res.to_whom)
        self.assertEqual('R', res.color)

    def test_tell_randomly_rank(self):
        res = utils.tell_randomly(0, self.info_player_0, 26)
        self.assertIsInstance(res, moves.HanabiDiscloseRankAction)
        self.assertEqual(0, res.player_id)
        self.assertEqual(1, res.to_whom)
        self.assertEqual(3, res.rank)

    def test_cannot_discard_randomly(self):
        self.info_player_0.disclosures = 8
        self.assertIsNone(utils.discard_randomly(0, self.info_player_0, 26))

    def test_discard_randomly(self):
        res = utils.discard_randomly(0, self.info_player_0, 26)
        self.assertIsInstance(res, moves.HanabiDiscardAction)
        self.assertEqual(0, res.player_id)
        self.assertEqual(1, res.card)

    def test_tell_unknown_cannot(self):
        self.info_player_0.known_info[1] = ['R1', 'W3']
        self.assertIsNone(utils.tell_unknown(0, self.info_player_0, 3))

    def test_tell_unknown_rank(self):
        res = utils.tell_unknown(0, self.info_player_0, 6)
        self.assertIsInstance(res, moves.HanabiDiscloseRankAction)
        self.assertEqual(0, res.player_id)
        self.assertEqual(1, res.to_whom)
        self.assertEqual(3, res.rank)

    def test_tell_unknown_color(self):
        res = utils.tell_unknown(0, self.info_player_0, 3)
        self.assertIsInstance(res, moves.HanabiDiscloseColorAction)
        self.assertEqual(0, res.player_id)
        self.assertEqual(1, res.to_whom)
        self.assertEqual('R', res.color)

    def test_tell_playable(self):
        res = utils.tell_playable(0, self.info_player_0, 3)
        self.assertIsInstance(res, moves.HanabiDiscloseColorAction)
        self.assertEqual(0, res.player_id)
        self.assertEqual(1, res.to_whom)
        self.assertEqual('Q', res.color)

    def test_tell_playable_none(self):
        res = utils.tell_playable(1, self.info_player_0, 2)
        self.assertIsNone(res)
