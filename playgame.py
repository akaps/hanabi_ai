import argparse
import time
from pydoc import locate
from tools.hanabi_table import HanabiTable
from tools.hanabi_card import HanabiColor
import sys
import logging
from tools.hanabi_moves import \
    HanabiDiscardAction, \
    HanabiPlayAction, \
    HanabiColorDiscloseAction, \
    HanabiRankDiscloseAction

def main(argv):
    args = parse_args()
    game = HanabiGame(args.players, args.seed, args.variant)
    game.play_game(args)

def parse_args():
    usage = "runs a game of Hanabi using the listed players"

    parser = argparse.ArgumentParser(description = usage)

    #Positional arguments
    parser.add_argument('players', nargs = '+', 
                        help = 'the players that will play Hanabi')

    #Optional arguments
    parser.add_argument('-s', '--seed', 
                        default = int(round(time.time()*1000)), type = int, 
                        help = 'a specific seed for shuffling the deck')
    parser.add_argument('-r', '--variant', type = int, choices = [1, 2, 3], 
                        dest = 'variant', 
                        help = 'play the selected variant')
    parser.add_argument('-l', '--log_dir', dest = 'log_dir', default = None, 
                        help = 'directory to save results to')
    parser.add_argument("-v", "--verbose", dest = "verbose",
                         action = 'store_true',
                         help="print out moves as game goes")
    parser.add_argument('-e', '--log_stderr', dest = 'log_stderr',
                         action='store_true',
                         help='additionally log players errors to stderr')

    return parser.parse_args()

def prep_players(player_names):
    return map(lambda player_name: locate(player_name)(), player_names)

class HanabiGame:
    def __init__(self, players, seed, variant):
        logger = logging.getLogger('example')
        logger.setLevel(logging.INFO)
        self.players = prep_players(players)
        self.table = HanabiTable(len(players), seed, variant)
        self.variant = variant
        self.current_player = 0

    def play_game(self, verbose):
        def pretty_print_info(info):
            logging.info("-----")
            logging.info("Player {player_id} sees:".format(player_id = self.current_player))
            logging.info("Players: {players}".format(players = info["num_players"]))
            logging.info("Cards in deck: {deck}".format(deck = info["deck_size"]))
            logging.info("Discarded: {discard}".format(discard = info["discarded"]))
            logging.info("Score: {score}, Progress: {scored}".format(score = info["score"], scored = info["scored_cards"]))
            logging.info("Sees: {visible}".format(visible = info["hands"]))
            logging.info("Knows: {known}".format(known = info["known_info"]))
            logging.info("Disclosures left: {disclosures}".format(disclosures = info["disclosures"]))
            logging.info("Mistakes left: {mistakes}".format(mistakes = info["mistakes_left"]))
            logging.info("-----")

        while not self.table.is_game_over():
            player = self.players[self.current_player]
            info = self.table.info_for_player(self.current_player)
            player_move = player.do_turn(self.current_player, info)
            if verbose:
                pretty_print_info(info)
                logging.info("Player {player_id} played {move}".format(player_id = self.current_player, move = player_move))
            self.parse_turn(player_move)
            self.current_player = (self.current_player + 1) % self.table.num_players
        logging.info("Final score: {score}".format(score = self.table.score()))

    def is_valid_move(self, player_move):
        return HanabiPlayAction.can_parse_move(player_move) or \
            HanabiDiscardAction.can_parse_move(player_move) or \
            HanabiColorDiscloseAction.can_parse_move(player_move) or \
            HanabiRankDiscloseAction.can_parse_move(player_move)
            #validate discard is possible for the given table
            #validate disclose is possible for the given table

    def parse_turn(self, player_move):           
        if not self.is_valid_move(player_move):
            self.disqualify_and_exit(player_move)
        move = player_move["play_type"]
        if move == "play":
            self.table.play_card(self.current_player, player_move["card"])
        elif move == "discard":
            self.table.discard_card(self.current_player, player_move["card"])
        elif move == "disclose":
            self.play_disclose(player_move)

    def play_disclose(self, player_move):
        disclose_type = player_move["disclose_type"]
        if disclose_type == "color":
            self.table.disclose_color(self.current_player, player_move["player"], player_move["color"]),
        elif disclose_type == "rank":
            self.table.disclose_rank(self.current_player, player_move["player"], player_move["rank"])

    def disqualify_and_exit(self, bot_move):
        logging.error("Received invalid move from player {id}".format(id = self.current_player))
        logging.error(bot_move)
        logging.error("Expected format for play card:")
        logging.error("{'play_type':'play', 'card':<number>}")

        logging.error("Expected format for discard card:")
        logging.error("{'play_type':'discard', 'card':<number>}")
        
        logging.error("Expected format for disclose color:")
        logging.error("{'play_type':'disclose', 'disclose_type':'color, 'color':<color>}")
        logging.error("'color' cannot be '*' in a Variant 3 game")
        
        logging.error("Expected format for disclose rank:")
        logging.error("{'play_type':'disclose', 'disclose_type':'rank, 'rank':<number>}")
        exit()

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
