import argparse
import time
from pydoc import locate
from tools.hanabi_table import HanabiTable
from tools.hanabi_card import HanabiColor
import sys
import logging
import os
from tools.hanabi_moves import \
    HanabiDiscardAction, \
    HanabiPlayAction, \
    HanabiColorDiscloseAction, \
    HanabiRankDiscloseAction

logger = logging.getLogger(__name__)

def main(argv):
    args = parse_args()
    if args.is_tournament:
        run_tournament(args)
    else:
        run_one_game(args)

def generate_pairings(players):
    res = []
    for i in range(len(players)):
        for j in range(i + 1, len(players)):
            res.append([players[i], players[j]])
    return res

def friendly_name(player_name):
    return player_name[player_name.rfind(".") + 1:]

def generate_file_name(base_name, ext):
    #don't commit until this avoids overwriting previous file
    file_name = '{base_name}.{ext}'.format(
                base_name = base_name,
                ext = ext)
    #issue: running a tournament with mutliple bots of the same name causes a collision during scoring. Shouldn't be considered?
    attempt = 1
    while os.path.isfile(file_name):
        file_name = '{base_name}_{attempt}.{ext}'.format(
                base_name = base_name,
                attempt = attempt,
                ext = ext)
        attempt += 1
    return file_name

def tournament_file_names(args, player1, player2):
    log_name =  '{base}_{player1}_{player2}'.format(
                base = args.log_dir.split('.')[0],
                player1 = friendly_name(player1),
                player2 = friendly_name(player2))       
    log_dir = generate_file_name(log_name, args.log_dir.split('.')[1])
    error_name = '{base}_{player1}_{player2}'.format(
                base = args.log_stderr.split('.')[0],
                player1 = friendly_name(player1),
                player2 = friendly_name(player2))
    log_stderr = generate_file_name(error_name, args.log_stderr.split('.')[1])
    return log_dir, log_stderr

def run_tournament(args):
    tournament_scores = dict.fromkeys(args.players, 0)
    pairings = generate_pairings(args.players)
    for player1, player2 in pairings:
        log_dir, log_stderr = tournament_file_names(args, player1, player2)
        prep_logger(log_dir, args.verbose, log_stderr)
        
        game = HanabiGame([player1, player2], args.seed, args.variant)
        try:
            game.play_game(args)
            score = game.table.score()
        except:
            #if a player has messed up, penalize both
            #could diqualify the failing bot if we can determine who failed
            score = -25
        finally:
            logger.info('results for {player1}-{player2}:'.format(player1 = player1, player2 = player2))
            logger.info(score)

            tournament_scores[player1] += score
            tournament_scores[player2] += score
    tournament_scores = {k: v / len(pairings) for k, v in tournament_scores.iteritems()}
    logger.info(tournament_scores)
    winning_score = max(tournament_scores.itervalues())
    winners = [key for key, value in tournament_scores.items() if value == winning_score]
    if len(winners) == 1:
        logger.info('Winner is {winner}'.format(winner = winners[0]))
    else:
        logger.info('Winners are {winners}'.format(winners = winners))

def run_one_game(args):
    prep_logger(args.log_dir, args.verbose, args.log_stderr)
    game = HanabiGame(args.players, args.seed, args.variant)
    game.play_game(args)

def prep_logger(log_dir, verbose, log_stderr):
    logger.addHandler(logging.StreamHandler())
    if verbose:
        logger.setLevel(logging.INFO)
    if log_dir:
        fh = logging.FileHandler('results/{dir}'.format(dir = log_dir))
        logger.addHandler(fh)
    if log_stderr:
        efh = logging.FileHandler('results/{dir}'.format(dir = log_stderr))
        logger.addHandler(efh)

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
                        help = 'play the selected variant')
    parser.add_argument('-v', '--verbose', dest = 'verbose',
                        action = 'store_true',
                        help = 'log moves as game is played')
    parser.add_argument('-t', '--tournament', dest = 'is_tournament',
                        action = 'store_true',
                        help = 'runs 2 player games for all combinations of players (no repeats)')
    parser.add_argument('-l', '--log_dir', dest = 'log_dir', default = None, 
                        help = 'file to save results to')
    parser.add_argument('-e', '--log_stderr', dest = 'log_stderr',
                        help = 'additionally log player errors')

    return parser.parse_args()

def prep_players(player_names):
    return map(lambda player_name: locate(player_name)(), player_names)

class HanabiGame:
    def __init__(self, players, seed, variant):
        self.players = prep_players(players)
        self.table = HanabiTable(len(players), seed, variant)
        self.variant = variant
        self.current_player = 0

    def play_game(self, verbose):
        def pretty_print_info(info):
            logger.info('-----')
            logger.info('Player {player_id} sees:'.format(player_id = self.current_player))
            logger.info('Players: {players}'.format(players = info['num_players']))
            logger.info('Cards in deck: {deck}'.format(deck = info['deck_size']))
            logger.info('Discarded: {discard}'.format(discard = info['discarded']))
            logger.info('Score: {score}'.format(score = info['score']))
            logger.info('Progress: {scored}'.format(scored = info['scored_cards']))
            logger.info('Sees: {visible}'.format(visible = info['hands']))
            logger.info('Knows: {known}'.format(known = info['known_info']))
            logger.info('Disclosures left: {disclosures}'.format(disclosures = info['disclosures']))
            logger.info('Mistakes left: {mistakes}'.format(mistakes = info['mistakes_left']))
            logger.info('-----')

        while not self.table.is_game_over():
            player = self.players[self.current_player]
            info = self.table.info_for_player(self.current_player)
            player_move = player.do_turn(self.current_player, info)
            move = self.parse_turn(player_move)
            pretty_print_info(info)
            logger.info(str(move))
            self.current_player = (self.current_player + 1) % self.table.num_players
        logger.info('-----')
        self.game_history()
        logger.info('Final score: {score}'.format(score = self.table.score()))

    def game_history(self):
        moves = map(lambda action: str(action), self.table.history)
        for move in moves:
            logger.info(move)

    def is_valid_move(self, player_move):
        return HanabiPlayAction.can_parse_move(player_move) or \
            (HanabiDiscardAction.can_parse_move(player_move) and self.table.can_discard()) or \
            (self.table.can_disclose() and \
                (HanabiColorDiscloseAction.can_parse_move(player_move) or \
                HanabiRankDiscloseAction.can_parse_move(player_move)))

    def parse_turn(self, player_move):
        if not self.is_valid_move(player_move):
            self.disqualify_and_exit(player_move)
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

    def disqualify_and_exit(self, bot_move):
        logging.error('Received invalid move from player {id}'.format(id = self.current_player))
        logging.error(bot_move)
        logging.error('Expected format for play card:')
        logging.error('{"play_type":"play", "card":<number>}')

        logging.error('Expected format for discard card:')
        logging.error('{"play_type":"discard", "card":<number>}')
        
        logging.error('Expected format for disclose color:')
        logging.error('{"play_type":"disclose", "disclose_type":"color, "color":<color>}')
        logging.error('"color" cannot be "*" in a Variant 3 game')
        
        logging.error('Expected format for disclose rank:')
        logging.error('{"play_type":"disclose", "disclose_type":"rank, "rank":<number>}')
        exit()

if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
