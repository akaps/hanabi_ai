import unittest
from hanabi_ai.model.game_info import GameInfo

class GameInfoTests(unittest.TestCase):
    def setUp(self):
        #a simulated game state 7 turns in
        self.info_player_0 = GameInfo()
        self.info_player_0.score = 2
        self.info_player_0.deck_size = 36
        self.info_player_0.discarded = ['G1', 'Y1']
        self.info_player_0.disclosures = 5
        self.info_player_0.mistakes_left = 5
        self.info_player_0.num_players = 2
        self.info_player_0.hands = [
            ['??', '??', '??', '??', '??'],
            ['R3', 'R2', 'W3', 'B5', 'G4']
        ],
        self.info_player_0.known_info = [
            ['??', '??', '??', '??', '?1'],
            ['??', '??', '??', '??', '??']
        ]
        self.info_player_0.scored_cards = {
            'R' : 0,
            'B' : 0,
            'G' : 0,
            'Y' : 1,
            'W' : 1
        }
        self.info_player_0.history = []

    def test_can_discard(self):
        self.assertTrue(self.info_player_0.can_discard())

    def test_cannot_discard(self):
        self.info_player_0.disclosures = 8
        self.assertFalse(self.info_player_0.can_discard())

    def test_can_disclose(self):
        self.assertTrue(self.info_player_0.can_disclose())

    def test_cannot_disclose(self):
        self.info_player_0.disclosures = 0
        self.assertFalse(self.info_player_0.can_disclose())

    def test_is_safe(self):
        self.assertTrue(self.info_player_0.is_safe('W2'))

    def test_is_not_safe(self):
        self.assertFalse(self.info_player_0.is_safe('W3'))

    def test_next_player(self):
        self.assertEqual(1, self.info_player_0.next_player(0))
        self.assertEqual(0, self.info_player_0.next_player(1))

    def test_next_player_more_players(self):
        self.info_player_0.num_players = 4
        self.assertEqual(1, self.info_player_0.next_player(0))
        self.assertEqual(2, self.info_player_0.next_player(1))
        self.assertEqual(3, self.info_player_0.next_player(2))
        self.assertEqual(0, self.info_player_0.next_player(3))
