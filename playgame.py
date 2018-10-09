import argparse
import time
from pydoc import locate
from tools.hanabi_table import HanabiTable
from tools.hanabi_card import HanabiColor
import sys
import logging
from logging.handlers import RotatingFileHandler
from tools.hanabi_moves import \
    HanabiDiscardAction, \
    HanabiPlayAction, \
    HanabiColorDiscloseAction, \
    HanabiRankDiscloseAction

def main(argv):
    args = parse_args()
    logger = prep_logger(args.log_dir, args.verbose, args.log_stderr, len(args.players))
    if args.is_tournament:
        run_tournament(args, logger)
    else:
        run_one_game(args, logger)

def generate_pairings(players):
    res = []
    for i in range(len(players)):
        for j in range(i + 1, len(players)):
            res.append([players[i], players[j]])
    return res

def run_tournament(args, logger):
    tournament_scores = dict.fromkeys(args.players, 0)
    pairings = generate_pairings(args.players)
    for player1, player2 in pairings:
        try:
            game = HanabiGame([player1, player2], args.seed, args.variant)
            game.play_game(args, logger)
            score = game.table.score()
        except:
            #if a player has messed up, penalize both
            #could diqualify the failing bot if we can determine who failed
            logger.warning("{player1} or {player2} failed to complete a game".format(
                player1 = player1,
                player2 = player2
                ))
            score = -25
        finally:
            for handler in logger.handlers:
                if handler.__class__ is RotatingFileHandler:
                    handler.doRollover()
            tournament_scores[player1] += score
            tournament_scores[player2] += score
    tournament_scores = {k: v / len(pairings) for k, v in tournament_scores.iteritems()}
    logger.info("Scores: {scores}".format(scores = tournament_scores))
    winning_score = max(tournament_scores.itervalues())
    winners = [key for key, value in tournament_scores.items() if value == winning_score]
    if len(winners) == 1:
        logger.info('Winner is {winner}'.format(winner = winners[0]))
    else:
        logger.info('Winners are {winners}'.format(winners = winners))

def run_one_game(args, logger):
    game = HanabiGame(args.players, args.seed, args.variant)
    game.play_game(args, logger)

def prep_logger(log_dir, verbose, log_stderr, count):
    logging.basicConfig()
    logger = logging.getLogger(__name__)
    formatter = logging.Formatter('[%(asctime)s] %(levelname)8s --- %(message)s ' +
                                  '(%(filename)s:%(lineno)s)',datefmt='%Y-%m-%d %H:%M:%S')
    if verbose:
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.INFO)
    if log_dir:
        fh = RotatingFileHandler('results/{dir}'.format(dir = log_dir), mode = 'w', backupCount = count)
        fh.setLevel(logging.DEBUG)
        logger.addHandler(fh)
        fh.setFormatter(formatter)
    if log_stderr:
        efh = RotatingFileHandler('results/{dir}'.format(dir = log_stderr), mode = 'w', backupCount = count)
        efh.setLevel(logging.ERROR)
        logger.addHandler(efh)
        efh.setFormatter(formatter)
    return logger

def parse_args():
    usage = 'plays games of Hanabi using the listed players'

    parser = argparse.ArgumentParser(description = usage)

    #Positional arguments
    parser.add_argument('players', nargs = '+', 
                        help = 'the players that will play Hanabi. First 5 will play unless in tournament mode')

    #Optional arguments
    parser.add_argument('-s', '--seed', 
                        default = int(round(time.time()*1000)), type = int, 
                        help = 'a specific seed for shuffling the deck')
    parser.add_argument('-r', '--variant', type = int, choices = [1, 2, 3], 
                        dest = 'variant', 
                        help = 'plays the selected variant')
    parser.add_argument('-t', '--tournament', dest = 'is_tournament',
                        action = 'store_true',
                        help = 'runs 2 player games for all combinations of players (no repeats)')
    parser.add_argument('-v', '--verbose', dest = 'verbose',
                        action = 'store_true',
                        help = 'logs moves and game state as game is played')
    parser.add_argument('-l', '--log_dir', dest = 'log_dir', default = None, 
                        help = 'saves logs to file')
    parser.add_argument('-e', '--log_stderr', dest = 'log_stderr',
                        help = 'log errors to file')

    return parser.parse_args()

def prep_players(player_names):
    return map(lambda player_name: locate(player_name)(), player_names)

class HanabiGame:
    def __init__(self, players, seed, variant):
        self.players = prep_players(players)
        self.table = HanabiTable(len(players), seed, variant)
        self.variant = variant
        self.current_player = 0

    def play_game(self, verbose, logger):
        def pretty_print_info(info):
            logger.debug('Player {player_id} sees:'.format(player_id = self.current_player))
            logger.debug('Players: {players}'.format(players = info['num_players']))
            logger.debug('Cards in deck: {deck}'.format(deck = info['deck_size']))
            logger.debug('Discarded: {discard}'.format(discard = info['discarded']))
            logger.debug('Score: {score}'.format(score = info['score']))
            logger.debug('Progress: {scored}'.format(scored = info['scored_cards']))
            logger.debug('Sees: {visible}'.format(visible = info['hands']))
            logger.debug('Knows: {known}'.format(known = info['known_info']))
            logger.debug('Disclosures left: {disclosures}'.format(disclosures = info['disclosures']))
            logger.debug('Mistakes left: {mistakes}'.format(mistakes = info['mistakes_left']))

        player_details = "Game with {players}".format(players = map(lambda(player): player.__class__.__name__, self.players))
        logger.info(player_details)
        logger.debug(player_details)

        while not self.table.is_game_over():
            player = self.players[self.current_player]
            info = self.table.info_for_player(self.current_player)
            player_move = player.do_turn(self.current_player, info)
            move = self.parse_turn(player_move, logger)
            pretty_print_info(info)
            logger.debug(str(move))
            self.current_player = (self.current_player + 1) % self.table.num_players
        for move in self.game_history():
            logger.debug(move)
        logger.info('Final score: {score}'.format(score = self.table.score()))

    def game_history(self):
        moves = map(lambda action: str(action), self.table.history)
        return moves

    def is_valid_move(self, player_move):
        return HanabiPlayAction.can_parse_move(player_move) or \
            (HanabiDiscardAction.can_parse_move(player_move) and self.table.can_discard()) or \
            (self.table.can_disclose() and \
                (HanabiColorDiscloseAction.can_parse_move(player_move) or \
                HanabiRankDiscloseAction.can_parse_move(player_move)))

    def parse_turn(self, player_move, logger):
        if not self.is_valid_move(player_move):
            self.disqualify_and_exit(player_move, logger)
        move = player_move['play_type']
        if move == 'play':
            return self.table.play_card(self.current_player, player_move['card'])
        elif move == 'discard':
            return self.table.discard_card(self.current_player, player_move['card'])
        elif move == 'disclose':
            return self.play_disclose(player_move)

    def play_disclose(self, player_move):
        disclose_type = player_move['disclose_type']
        if disclose_type == 'color':
            return self.table.disclose_color(self.current_player, player_move['player'], player_move['color'])
        elif disclose_type == 'rank':
            return self.table.disclose_rank(self.current_player, player_move['player'], player_move['rank'])

    def disqualify_and_exit(self, bot_move, logger):
        logger.error('Received invalid move from player {id}'.format(id = self.current_player))
        logger.error(bot_move)
        logger.error('Expected format for play card:')
        logger.error('{"play_type":"play", "card":<number>}')

        logger.error('Expected format for discard card:')
        logger.error('{"play_type":"discard", "card":<number>}')
        
        logger.error('Expected format for disclose color:')
        logger.error('{"play_type":"disclose", "disclose_type":"color, "color":<color>}')
        logger.error('"color" cannot be "*" in a Variant 3 game')
        
        logger.error('Expected format for disclose rank:')
        logger.error('{"play_type":"disclose", "disclose_type":"rank, "rank":<number>}')
        exit(1)

if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
