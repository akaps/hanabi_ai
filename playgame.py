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
    usage = "runs a game of Hanabi using the listed bots"

    parser = argparse.ArgumentParser(description = usage)

    #Positional arguments
    parser.add_argument('bots', nargs = '+', 
                        help = 'the bots that will play Hanabi')

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
                         help='additionally log bot errors to stderr')

    return parser.parse_args()

def prep_bots(bot_names):
    res = []
    for bot_name in bot_names:
        bot_class = locate(bot_name)
        res.append(bot_class())
    return res

class HanabiGame:
    def __init__(self, args):
        self.bots = prep_bots(args.bots)
        self.table = HanabiTable(len(args.bots), args.seed, args.variant)
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
            bot = self.bots[self.current_player]
            info = self.table.info_for_player(self.current_player)
            bot_move = bot.do_turn(self.current_player, info)
            if args.verbose:
                pretty_print_info(info)
                print("Player {player_id} played {move}".format(player_id = self.current_player, move = bot_move))
            self.parse_turn(bot_move)
            self.current_player = (self.current_player + 1) % self.table.num_players
        print("Final score: {score}".format(score = self.table.score()))

    def is_valid_move(self, bot_move):
        return "play" not in bot_move or \
            self.is_valid_play_move(bot_move) or \
            self.is_valid_discard_move(bot_move) or \
            self.is_valid_disclose_move(bot_move)

    def is_valid_play_move(self, bot_move):
        return bot_move["move"] == "play" and "card" in bot_move

    def is_valid_discard_move(self, bot_move):
        return self.table.can_discard() and bot_move["move"] == "discard"

    def is_valid_disclose_move(self, bot_move):
        if self.table.can_disclose() and bot_move["move"] == "disclose":
            return self.is_valid_disclose_color(bot_move) or self.is_valid_disclose_rank(bot_move)
        else:
            return False

    def is_valid_disclose_color(self, bot_move):
         return bot_move["disclose_type"] == "rank" and "color" in bot_move

    def is_valid_disclose_rank(self, bot_move):
        return bot_move["disclose_type"] == "rank" and "rank" in bot_move

    def parse_turn(self, bot_move):           
        if not self.is_valid_move(bot_move):
            self.disqualify_and_exit(bot_move)
        move = bot_move["move"]
        if move == "play":
            self.table.play_card(self.current_player, bot_move["card"])
        elif move == "discard":
            self.table.discard_card(self.current_player, bot_move["card"])
        elif move == "disclose":
            self.play_disclose(bot_move)

    def play_disclose(self, bot_move):
        disclose_type = bot_move["disclose_type"]
        if disclose_type == "color":
            self.table.disclose_color(self.current_player, bot_move["color"]),
        elif disclose_type == "rank":
            self.table.disclose_rank(self.current_player, bot_move["rank"])

    def disqualify_and_exit(self, bot_move):
        print("Received invalid move from player {id}".format(id = self.current_player))
        print(bot_move)
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
