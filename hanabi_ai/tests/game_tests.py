import unittest
from argparse import Namespace
from hanabi_ai.play_game import HanabiGame
from hanabi_ai.model.deck import HanabiVariant
import hanabi_ai.model.moves as moves
from hanabi_ai.model.game_info import GameInfo

def prep_args():
    args = Namespace()
    args.seed = 0
    args.variant = HanabiVariant.basic
    player_name = 'hanabi_ai.players.example_discarder.Discarder'
    args.players = [
        player_name,
        player_name]
    args.seed = 0
    return args

class HanabiGameTests(unittest.TestCase):

    def setUp(self):
        args = prep_args()
        self.game = HanabiGame(args.players, args.seed, args.variant)
        self.play = moves.HanabiPlayAction(0, 0)
        self.discard = moves.HanabiDiscardAction(0, 0)
        self.disclose_color = moves.HanabiDiscloseColorAction(0, 1, 'R')
        self.disclose_rank = moves.HanabiDiscloseRankAction(0, 1, 2)
        self.game_info = GameInfo()

    def test_is_valid_move(self):
        self.game_info.disclosures = 6
        self.game.table.disclose_rank(0, 0, 1)
        self.assertTrue(self.play.is_valid(self.game_info))
        self.assertTrue(self.discard.is_valid(self.game_info))
        self.assertTrue(self.disclose_color.is_valid(self.game_info))
        self.assertTrue(self.disclose_rank.is_valid(self.game_info))
