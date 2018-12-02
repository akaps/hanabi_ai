import argparse
import time
import os
from pydoc import locate
import sys
import logging
from logging.handlers import RotatingFileHandler
import itertools
from sets import Set
import matplotlib
matplotlib.use('TkAgg') #pylint: disable=wrong-import-position
import matplotlib.pyplot as plt
import numpy
from hanabi_ai.model.hanabi_table import HanabiTable
from hanabi_ai.model.hanabi_deck import HanabiVariant
from hanabi_ai.players.hanabi_player import HanabiPlayer

logging.basicConfig()
LOGGER = logging.getLogger(__name__)

class InvalidHanabiMoveException(Exception):
    def __init__(self, message, player_id):
        super(InvalidHanabiMoveException, self).__init__(message)
        self.player_id = player_id

def main(argv):
    args = parse_args(argv)
    prep_logger(args.log_dir, args.verbose, args.log_stderr, len(args.players)*args.iterations)
    args.players = validate_players(args.players)
    if args.command == 'tournament':
        run_tournament(args)
    else:
        run_one_configuration(args)

def validate_players(players):
    return [player for player in players if locate(player) is not None and
            isinstance(locate(player)(), HanabiPlayer)]

def rotate_logs():
    for handler in LOGGER.handlers:
        if handler.__class__ is RotatingFileHandler:
            handler.doRollover()

def disqualify_player(disqualified, tournament_scores, player):
    disqualified.add(player)
    for disqualify in disqualified:
        if disqualify in tournament_scores:
            del tournament_scores[disqualify]
    LOGGER.warning('removed player %s from tournament', disqualified)

def ensure_path(path):
    directories_from_path = os.path.dirname(path)
    if directories_from_path and not os.path.isdir(directories_from_path):
        os.makedirs(directories_from_path)

def run_tournament(args):
    tournament_scores = dict.fromkeys(args.players, [])
    pairings = list(itertools.combinations(args.players, args.per_round))
    disqualified = Set()
    for players in pairings:
        if set(players).issubset(disqualified):
            continue
        try:
            for _ in range(args.iterations):
                score = run_one_game(players, args.seed, args.variant)
                for player in players:
                    tournament_scores[player].append(score)
        except InvalidHanabiMoveException as err:
            disqualify_player(disqualified,
                              tournament_scores,
                              players[err.player_id])
        finally:
            rotate_logs()
    tournament_results = {
        key: {
            'mean': numpy.mean(val),
            'variance' : numpy.var(val)
            }
        for key, val in tournament_scores.iteritems()
        }

    LOGGER.info('Scores: %s', tournament_scores)
    LOGGER.info('Results: %s', tournament_results)
    determine_winner(tournament_results)
    if args.show_graphs:
        show_plot(tournament_scores)

def show_plot(scores):
    means = [numpy.mean(score) for score in scores.values()]
    std = [numpy.std(score) for score in scores.values()]
    labels = [name for name in scores.keys()]
    ind = numpy.arange(len(labels))
    width = 0.35
    plt.bar(ind, means, width, yerr=std)
    plt.ylabel('scores')
    plt.title('Scores by player')
    plt.xticks(ind, labels)
    plt.yticks(numpy.arange(0, 26, 5))
    plt.show()

def determine_winner(results):
    winning_average = max(results.itervalues())['mean']
    average_winners = {key: val for key, val in results.items() if val['mean'] is winning_average}
    winning_variance = min(average_winners.itervalues())['variance']
    winners = [key for key, val in average_winners.items() if val['variance'] is winning_variance]
    LOGGER.info('Winner(s): %s', winners)
    return winners

def run_one_configuration(args):
    for _ in range(args.iterations):
        run_one_game(args.players, args.seed, args.variant)
        rotate_logs()

def run_one_game(players, seed, variant):
    game = HanabiGame(players, seed, HanabiVariant(variant))
    game.play_game()
    return game.table.score()

def prep_logger(log_dir, verbose, log_stderr, count):
    formatter = logging.Formatter('[%(asctime)s] %(levelname)8s --- %(message)s ' +
                                  '(%(filename)s:%(lineno)s)', datefmt='%Y-%m-%d %H:%M:%S')
    if verbose:
        LOGGER.setLevel(logging.DEBUG)
    else:
        LOGGER.setLevel(logging.INFO)
    if log_dir:
        ensure_path(log_dir)
        file_handler = RotatingFileHandler(log_dir, mode='w', backupCount=count)
        file_handler.setLevel(logging.DEBUG)
        LOGGER.addHandler(file_handler)
        file_handler.setFormatter(formatter)
    if log_stderr:
        ensure_path(log_stderr)
        error_file_handler = RotatingFileHandler(log_stderr, mode='w', backupCount=count)
        error_file_handler.setLevel(logging.ERROR)
        LOGGER.addHandler(error_file_handler)
        error_file_handler.setFormatter(formatter)

def parse_args(args):
    usage = 'plays games of Hanabi using the listed players'

    parent_parser = argparse.ArgumentParser(add_help=False)

    #Positional arguments
    parent_parser.add_argument('players',
                               nargs='+',
                               help='the players that will play Hanabi. '
                               'First 5 will play unless in tournament mode')

    #Optional arguments
    parent_parser.add_argument('-s', '--seed',
                               default=int(round(time.time()*1000)),
                               type=int,
                               help='a specific seed for shuffling the deck')
    parent_parser.add_argument('-r', '--variant',
                               type=int,
                               choices=[1, 2, 3],
                               default=0,
                               dest='variant',
                               help='play the selected variant')
    parent_parser.add_argument('-i', '--game_iterations',
                               type=int,
                               default=1,
                               dest='iterations',
                               help='number of times to play each game')
    parent_parser.add_argument('-v', '--verbose',
                               dest='verbose',
                               action='store_true',
                               help='log moves and game state as game is played')
    parent_parser.add_argument('-l', '--log_dir',
                               dest='log_dir',
                               default=None,
                               help='save logs to file')
    parent_parser.add_argument('-e', '--log_stderr',
                               dest='log_stderr',
                               help='log errors to file')

    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(help=usage,
                                       dest='command')

    #single game-specific arguments
    subparsers.add_parser('single',
                          help='run a single game of Hanabi',
                          parents=[parent_parser])

    #tournament mode-specific arguments
    tournament = subparsers.add_parser('tournament',
                                       parents=[parent_parser],
                                       help='run games for all combinations '
                                       'of players (no repeats)')
    tournament.add_argument('-p', '--players_per_game',
                            dest='per_round',
                            type=int,
                            choices=[2, 3, 4, 5],
                            default=2,
                            help='number of players per game in the tournament')
    tournament.add_argument('-g', '--graphs',
                            dest='show_graphs',
                            action='store_true',
                            help='show graphical results of tournament')
    return parser.parse_args(args)

def prep_players(player_names):
    return [locate(name)() for name in player_names]

class HanabiGame(object):
    def __init__(self, players, seed, variant):
        self.players = prep_players(players)
        self.table = HanabiTable(len(players), seed, variant)
        self.variant = variant
        self.current_player = 0

    def play_game(self):
        def pretty_print_info(info):
            LOGGER.debug('Player %s sees:', self.current_player)
            LOGGER.debug('Players: %s', info.num_players)
            LOGGER.debug('Cards in deck: %s', info.deck_size)
            LOGGER.debug('Discarded: %s', info.discarded)
            LOGGER.debug('Score: %s', info.score)
            LOGGER.debug('Progress: %s', info.scored_cards)
            LOGGER.debug('Sees: %s', info.hands)
            LOGGER.debug('Knows: %s', info.known_info)
            LOGGER.debug('Disclosures left: %s', info.disclosures)
            LOGGER.debug('Mistakes left: %s', info.mistakes_left)

        player_details = 'Game with {players}'.format(
            players=[player.__class__.__name__ for player in self.players])
        LOGGER.info(player_details)

        while not self.table.is_game_over():
            player = self.players[self.current_player]
            info = self.table.info_for_player(self.current_player)
            player_move = player.do_turn(self.current_player, info)
            if player_move.is_valid(info):
                player_move.execute(self.table)
                pretty_print_info(info)
                LOGGER.debug(str(player_move))
                self.current_player = (self.current_player + 1) % self.table.num_players
            else:
                self.disqualify(player_move)
        for move in self.game_history():
            LOGGER.debug(move)
        LOGGER.info('Final score: %s', self.table.score())

    def game_history(self):
        return [str(action) for action in self.table.history]

    def disqualify(self, player_move):
        LOGGER.warning('Expected format for play card:')
        LOGGER.warning('{"play_type":"play", "card":<number>}')

        LOGGER.warning('Expected format for discard card:')
        LOGGER.warning('{"play_type":"discard", "card":<number>}')

        LOGGER.warning('Expected format for disclose color:')
        LOGGER.warning('{"play_type":"disclose", "disclose_type":"color, "color":<color>}')
        LOGGER.warning('"color" cannot be "*" in a Variant 3 game')

        LOGGER.warning('Expected format for disclose rank:')
        LOGGER.warning('{"play_type":"disclose", "disclose_type":"rank, "rank":<number>}')
        LOGGER.error('Received invalid move from player %s: %s',
                     self.current_player,
                     player_move)
        raise InvalidHanabiMoveException('Received invalid move from player', self.current_player)

if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
