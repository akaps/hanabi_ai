import unittest
from tools.hanabi_moves import (HanabiDiscardAction,
    HanabiPlayAction,
    HanabiDiscloseColorAction,
    HanabiDiscloseRankAction)
from tools.hanabi_game_info import GameInfo

class HanabiMoveTests(unittest.TestCase):

    def setUp(self):
        self.play = HanabiPlayAction(0, 1)
        self.discard = HanabiDiscardAction(0, 1)
        self.color_disclose = HanabiDiscloseColorAction(0, 1, 'R')
        self.rank_disclose = HanabiDiscloseRankAction(0, 1, 1)
        self.game_info = GameInfo()

    def test_is_valid_play_move(self):
        self.assertTrue(self.play.is_valid(self.game_info))

    def test_is_valid_discard_move(self):
        self.game_info.disclosures = 0
        self.assertTrue(self.discard.is_valid(self.game_info))

    def test_is_valid_discard_move_cannot_discrd(self):
        self.game_info.disclosures = 8
        self.assertFalse(self.discard.is_valid(self.game_info))

    def test_is_valid_disclose_move(self):
        self.game_info.disclosures = 8
        self.assertTrue(self.color_disclose.is_valid(self.game_info))
        self.assertTrue(self.rank_disclose.is_valid(self.game_info))

    def test_is_valid_disclose_move_cannot_disclose(self):
        self.game_info.disclosures = 0
        self.assertFalse(self.color_disclose.is_valid(self.game_info))
        self.assertFalse(self.rank_disclose.is_valid(self.game_info))
