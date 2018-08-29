import argparse
import time
from pydoc import locate
from tools.hanabi_table import HanabiTable
import sys

def main(argv):
    usage ="rus a game of Hanabi using the listed bots"

    parser = argparse.ArgumentParser(description=usage)

    #Positional arguments
    parser.add_argument('bots', nargs='+', 
                        help = 'the bots that will play Hanabi')

    #Optional arguments
    parser.add_argument('-s', '--seed', 
                        default = int(round(time.time()*1000)), type = int, 
                        help = 'a specific seed for shuffling the deck')
    parser.add_argument('-r', '--rainbow', action = "store_true", 
                        dest = 'wild_included', 
                        help = 'play with the wildcard suit')
    parser.add_argument('-l', '--log_dir', dest = 'log_dir', default = None, 
                        help = 'directory to save results to')
    parser.add_argument("-v", "--verbose", dest="verbose",
                         action='store_true',
                         help="print out moves as game goes.")
    parser.add_argument('-e', '--log_stderr', dest='log_stderr',
                         action='store_true',
                         help='additionally log bot errors to stderr')

    args = parser.parse_args()
    game = HanabiGame(args)
    game.playGame(args)

def prepBots(botNames):
    res = []
    for botName in botNames:
        bot_class = locate(botName)
        res.append(bot_class())
    return res

class HanabiGame:
    def __init__(self, args):
        self.bots = prepBots(args.bots)
        self.table = HanabiTable(len(args.bots), args.seed, args.wild_included)
        self.currentPlayer = 0

    def playGame(self, args):
        def prettyPrintInfo(info):
            print("-----")
            print("Player {player_id} sees:".format(player_id = self.currentPlayer))
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
            bot = self.bots[self.currentPlayer]
            info = self.table.info_for_player(self.currentPlayer)
            if args.verbose:
                prettyPrintInfo(info)
            play = bot.do_turn(self.currentPlayer, info)

            print("Player {player_id} played {play}".format(player_id = self.currentPlayer,
                play = play))
            
            if play["move"] == "play" and "card" in play:
                self.table.play_card(self.currentPlayer, play["card"])
            elif play["move"] == "discard" and "card" in play:
                self.table.discard_card(self.currentPlayer, play["card"])
            elif play["move"] == "disclose":
                if play["disclose_type"] == "rank" and "rank" in play:
                    self.table.disclose_rank(play["disclose"], play["rank"])
                elif play["disclose_type"] == "color" and "color" in play:
                    self.table.disclose_color(play["disclose"], play["color"])
                else:
                    self.disqualify(self.currentPlayer, play)
                    exit()
            else:
                self.disqualify(self.currentPlayer, play)
                exit()
            self.currentPlayer = (self.currentPlayer + 1) % self.table.num_players
        print("Final score: {score}".format(score = self.table.score()))

    def disqualify(self, currentPlayer, play):
        print("Received invalid command from player {id}".format(id = currentPlayer))
        print(play)
        print("Expected format for play card:")
        print("{'play_type':'play', 'card':<number>}")

        print("Expected format for discard card:")
        print("{'play_type':'discard', 'card':<number>}")
        
        print("Expected format for disclose color:")
        print("{'play_type':'disclose', 'disclose_type':'color, 'color':<color>}")
        
        print("Expected format for disclose rank:")
        print("{'play_type':'disclose', 'disclose_type':'rank, 'rank':<number>}")

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))