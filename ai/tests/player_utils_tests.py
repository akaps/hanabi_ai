import unittest
import ai.player_utils as utils

class PlayerUtilsTests(unittest.TestCase):
    def setUp(self):
        #a simulated game state 7 turns in
        self.info_player_0 = {
            'score' : 2,
            'deck_size' : 36,
            'discarded' : ['G1', 'Y1'],
            'disclosures' : 5,
            'mistakes_left' : 2,
            'num_players' : 2,
            'hands' : [
                ['??', '??', '??', '??', '??'],
                ['R3', 'R2', 'W3', 'B5', 'G4']
            ],
            'known_info' : [
                ['??', '??', '??', '??', '?1'],
                ['??', '??', '??', '??', '??']
            ],
            'scored_cards' : {
                'R' : 0,
                'B' : 0,
                'G' : 0,
                'Y' : 1,
                'W' : 1
            },
            'history' : []
        }

    def test_discard_oldest_can_discard(self):
        expected = {
            'play_type' : 'discard',
            'card' : 0
        }
        actual = utils.discard_oldest_first(0, self.info_player_0)
        self.assertEquals(expected, actual)

    def test_discard_oldest_cannot_discard(self):
        self.info_player_0['disclosures'] = 8
        self.assertIsNone(utils.discard_oldest_first(0, self.info_player_0))

    def test_play_safe_card_can_play(self):
        self.info_player_0['known_info'][0][2] = 'R1'
        expected = {
            'play_type' : 'play',
            'card' : 2
        }
        actual = utils.play_safe_card(0, self.info_player_0)
        self.assertEquals(expected, actual)

    def test_play_safe_card_cannot_play(self):
        self.assertIsNone(utils.play_safe_card(0, self.info_player_0))
