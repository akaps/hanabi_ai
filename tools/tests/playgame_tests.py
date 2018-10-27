import playgame
import unittest
from sets import Set
from playgame import HanabiGame
from argparse import Namespace
from tools.hanabi_deck import HanabiVariant
from ai.hanabi_player import HanabiPlayer

class PlayGameparserTests(unittest.TestCase):

    def test_game_simple(self):
        args = ["single", "Discarder"]
        parsed = playgame.parse_args(args)
        print(parsed)
        self.assertEqual(1, len(parsed.players))
        self.assertEquals(0, parsed.variant)
        self.assertFalse(parsed.verbose)
        self.assertEquals(None, parsed.log_dir)
        self.assertEquals(None, parsed.log_stderr)
        self.assertEquals(parsed.command, 'single')

    def test_game_variant(self):
        args = ["single", "Discarder", '-r', '3']
        parsed = playgame.parse_args(args)
        self.assertEquals(3, parsed.variant)

    def test_game_verbose(self):
        args = ["single", "Discarder", '-v']
        parsed = playgame.parse_args(args)
        self.assertTrue(parsed.verbose)

    def test_game_log_dir(self):
        args = ["single", "Discarder", '-l', 'results.txt']
        parsed = playgame.parse_args(args)
        self.assertEquals("results.txt", parsed.log_dir)

    def test_game_log_stderr(self):
        args = ["single", "Discarder", '-e', 'errors.txt']
        parsed = playgame.parse_args(args)
        self.assertEquals("errors.txt", parsed.log_stderr)

    def test_game_seed(self):
        args = ["single", "Discarder", '-s', '76']
        parsed = playgame.parse_args(args)
        self.assertEquals(76, parsed.seed)

    def test_tournament_simple(self):
        args = ["tournament", "Discarder",]
        parsed = playgame.parse_args(args)
        self.assertEquals(2, parsed.per_round)
        self.assertEquals(parsed.command, 'tournament')

    def test_tournament_per_round(self):
        args = ["tournament", "Discarder", '-p', '4']
        parsed = playgame.parse_args(args)
        self.assertEquals(parsed.command, 'tournament')
        self.assertEquals(4, parsed.per_round)

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
        disqualified = Set()
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
        disqualified = Set()
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
        disqualified = Set()
        playgame.disqualify_player(disqualified, scores, 'A')
        playgame.disqualify_player(disqualified, scores, 'E')
        self.assertTrue('E', 'A' in disqualified)
        self.assertEqual(2, len(disqualified))
        self.assertTrue('A', 'E' not in scores)

    def test_determine_winner_one_winner(self):
        results = {
            'A' : {'mean': 20, 'variance': 2},
            'B' : {'mean': 22, 'variance': 7},
            'C' : {'mean': 25, 'variance': 25},
            'D' : {'mean': 25, 'variance': 4},
            'E' : {'mean': 25, 'variance': 1},
            'F' : {'mean': 1, 'variance': 1}
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
            'A' : {'mean': 20, 'variance': 2},
            'B' : {'mean': 22, 'variance': 7},
            'C' : {'mean': 25, 'variance': 25},
            'D' : {'mean': 25, 'variance': 4},
            'E' : {'mean': 25, 'variance': 4}
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
