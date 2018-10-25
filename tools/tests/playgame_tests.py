import playgame
import unittest
from playgame import HanabiGame
from argparse import Namespace
from tools.hanabi_deck import HanabiVariant
from ai.hanabi_player import HanabiPlayer

class MockBadPlayer:
    pass

class PlayGameTests(unittest.TestCase):

    def setUp(self):
        pass

    def test_validate_players(self):
        players = ['ai.example_discarder.Discarder', #valid player
                    'ai.example.missing.Missing', #missing player
                    'MockBadPlayer'] #player that does not implement HanabiPlayer
        prepped_players = ['ai.example_discarder.Discarder']
        self.assertEqual(prepped_players, playgame.validate_players(players))

    def test_disqualify_player_scored(self):
        scores = {
            'A' : 0,
            'B' : 20, #C did not have a game yet
            'D' : 50,
            'E' : 20
        }
        disqualified = []
        playgame.disqualify_player(disqualified, scores, 'D')
        self.assertTrue('D' in disqualified)
        self.assertEqual(1, len(disqualified))
        self.assertTrue('D' not in scores)

    def test_disqualify_player__not_scored(self):
        scores = {
            'A' : 0,
            'B' : 20, #C did not have a game yet
            'D' : 50,
            'E' : 20
        }
        disqualified = []
        playgame.disqualify_player(disqualified, scores, 'C')
        self.assertTrue('C' in disqualified)
        self.assertEqual(1, len(disqualified))
        self.assertTrue('C' not in scores)

    def test_disqualify_player__multiple(self):
        scores = {
            'A' : 0,
            'B' : 20, #C did not have a game yet
            'D' : 50,
            'E' : 20
        }
        disqualified = []
        playgame.disqualify_player(disqualified, scores, 'A')
        playgame.disqualify_player(disqualified, scores, 'E')
        self.assertTrue('E', 'A' in disqualified)
        self.assertEqual(2, len(disqualified))
        self.assertTrue('A', 'E' not in scores)

    def test_determine_winner_one_winner(self):
        results = {
            'A' : [20, 2],
            'B' : [22, 7],
            'C' : [25, 25],
            'D' : [25, 4],
            'E' : [25, 1],
            'F' : [1, 1]
        }
        winners = playgame.determine_winner(results)
        self.assertTrue('A' not in winners)
        self.assertTrue('B' not in winners)
        self.assertTrue('C' not in winners)
        self.assertTrue('D' not in winners)
        self.assertTrue('E' in winners)
        self.assertTrue('F' not in winners)

    def test_determine_winner_tie(self):
        results = {
            'A' : [20, 2],
            'B' : [22, 7],
            'C' : [25, 25],
            'D' : [25, 4],
            'E' : [25, 4]
        }
        winners = playgame.determine_winner(results)
        self.assertTrue('A' not in winners)
        self.assertTrue('B' not in winners)
        self.assertTrue('C' not in winners)
        self.assertTrue('D' in winners)
        self.assertTrue('E' in winners)

    def test_prep_players(self):
        init_players = playgame.prep_players(['ai.example_discarder.Discarder'])
        self.assertTrue(isinstance(init_players[0], HanabiPlayer))
