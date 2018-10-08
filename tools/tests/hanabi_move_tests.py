import unittest
from tools.hanabi_moves import (HanabiDiscardAction,
    HanabiPlayAction,
    HanabiColorDiscloseAction,
    HanabiRankDiscloseAction)

class HanabiMoveTests(unittest.TestCase):

    def setUp(self):
        self.well_formed_play = {'play_type':'play', 'card':1}
        self.malformed_play = {'play_type':'play'}
        self.well_formed_discard = {'play_type':'discard', 'card':1}
        self.malformed_discard = {}
        self.well_formed_color_disclose = {'play_type':'disclose', 'player':0, 'disclose_type':'color', 'color':'R'}
        self.malformed_color_disclose = {'play_type':'disclose', 'player':0, 'disclose_type':'color', 'color':'S'}
        self.well_formed_rank_disclose = {'play_type':'disclose', 'player':0, 'disclose_type':'rank', 'rank':2}
        self.malformed_rank_disclose = {'play_type':'disclose', 'player':0, 'disclose_type':'RANK', 'rank':7}

    def test_is_valid_play_move(self):
        self.assertTrue(HanabiPlayAction.can_parse_move(self.well_formed_play))
        self.assertFalse(HanabiPlayAction.can_parse_move(self.malformed_play))
        self.assertFalse(HanabiPlayAction.can_parse_move(self.well_formed_discard))

    def test_is_valid_discard_move(self):
        self.assertTrue(HanabiDiscardAction.can_parse_move(self.well_formed_discard))
        self.assertTrue(HanabiDiscardAction.can_parse_move(self.well_formed_discard))
        self.assertFalse(HanabiDiscardAction.can_parse_move(self.malformed_discard))
        self.assertFalse(HanabiDiscardAction.can_parse_move(self.well_formed_play))

    def test_is_valid_disclose_move(self):
        self.assertTrue(HanabiColorDiscloseAction.can_parse_move(self.well_formed_color_disclose))
        self.assertFalse(HanabiColorDiscloseAction.can_parse_move(self.well_formed_rank_disclose))
        self.assertFalse(HanabiColorDiscloseAction.can_parse_move(self.malformed_color_disclose))
        self.assertFalse(HanabiColorDiscloseAction.can_parse_move(self.malformed_rank_disclose))
        self.assertFalse(HanabiColorDiscloseAction.can_parse_move(self.well_formed_discard))

    def test_is_valid_disclose_color(self):
        self.assertTrue(HanabiColorDiscloseAction.can_parse_move(self.well_formed_color_disclose))
        self.assertFalse(HanabiColorDiscloseAction.can_parse_move(self.malformed_color_disclose))
        self.assertFalse(HanabiColorDiscloseAction.can_parse_move(self.well_formed_rank_disclose))

    def test_is_valid_disclose_rank(self):
        self.assertTrue(HanabiRankDiscloseAction.can_parse_move(self.well_formed_rank_disclose))
        self.assertFalse(HanabiRankDiscloseAction.can_parse_move(self.malformed_rank_disclose))
        self.assertFalse(HanabiRankDiscloseAction.can_parse_move(self.well_formed_color_disclose))
