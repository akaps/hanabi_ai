import argparse
import time
from pydoc import locate
from tools.hanabi_table import HanabiTable
from tools.hanabi_card import HanabiColor
import sys

def main(argv):
    args = parse_args()
    game = HanabiGame(args)
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
    return map(lambda: player_name: locate(player_name), player_names)

class HanabiGame:
    def __init__(self, args):
        self.players = prep_players(args.players)
        self.table = HanabiTable(len(args.players), args.seed, args.variant)
        self.variant = args.variant
        self.current_player = 0

    def play_game(self, args):
        def pretty_print_info(info):
            print("-----")
            print("Player {player_id} sees:".format(player_id = self.current_player))
            print("Players: {players}".format(players = info["num_players"]))
            print("Cards in deck: {deck}".format(deck = info["deck_size"]))
            print("Discarded: {discard}".format(discard = info["discarded"]))
            print("Score: {score}, Progress: {scored}".format(score = info["score"], scored = info["scored_cards"]))
            print("Sees: {visible}".format(visible = info["hands"]))
            print("Knows: {known}".format(known = info["known_info"]))
            print("Disclosures left: {disclosures}".format(disclosures = info["disclosures"]))
            print("Mistakes left: {mistakes}".format(mistakes = info["mistakes_left"]))
            print("-----")
            
        while not self.table.is_game_over():
            player = self.players[self.current_player]
            info = self.table.info_for_player(self.current_player)
            player_move = player.do_turn(self.current_player, info)
            if args.verbose:
                pretty_print_info(info)
                print("Player {player_id} played {move}".format(player_id = self.current_player, move = player_move))
            self.parse_turn(player_move)
            self.current_player = (self.current_player + 1) % self.table.num_players
        print("Final score: {score}".format(score = self.table.score()))

    def is_valid_move(self, player_move):
        return "play" not in player_move or \
            self.is_valid_play_move(player_move) or \
            self.is_valid_discard_move(player_move) or \
            self.is_valid_disclose_move(player_move)

    def is_valid_play_move(self, player_move):
        return player_move["move"] == "play" and "card" in player_move

    def is_valid_discard_move(self, player_move):
        return self.table.can_discard() and player_move["move"] == "discard"

    def is_valid_disclose_move(self, player_move):
        if self.table.can_disclose() and player_move["move"] == "disclose":
            return self.is_valid_disclose_color(player_move) or self.is_valid_disclose_rank(player_move)
        else:
            return False

    def is_valid_disclose_color(self, player_move):
         return player_move["disclose_type"] == "rank" and "color" in player_move

    def is_valid_disclose_rank(self, player_move):
        return player_move["disclose_type"] == "rank" and "rank" in player_move

    def parse_turn(self, player_move):           
        if not self.is_valid_move(player_move):
            self.disqualify_and_exit(player_move)
        move = player_move["move"]
        if move == "play":
            self.table.play_card(self.current_player, player_move["card"])
        elif move == "discard":
            self.table.discard_card(self.current_player, player_move["card"])
        elif move == "disclose":
            self.play_disclose(player_move)

    def play_disclose(self, player_move):
        disclose_type = player_move["disclose_type"]
        if disclose_type == "color":
            self.table.disclose_color(self.current_player, player_move["color"]),
        elif disclose_type == "rank":
            self.table.disclose_rank(self.current_player, player_move["rank"])

    def disqualify_and_exit(self, player_move):
        print("Received invalid move from player {id}".format(id = self.current_player))
        print(player_move)
        print("Expected format for play card:")
        print("{'play_type':'play', 'card':<number>}")

        print("Expected format for discard card:")
        print("{'play_type':'discard', 'card':<number>}")
        
        print("Expected format for disclose color:")
        print("{'play_type':'disclose', 'disclose_type':'color, 'color':<color>}")
        print("'color' cannot be '*' in a Variant 3 game")
        
        print("Expected format for disclose rank:")
        print("{'play_type':'disclose', 'disclose_type':'rank, 'rank':<number>}")
        exit()

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
