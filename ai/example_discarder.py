import tools.hanabi_table as game
import tools.hanabi_moves as moves
from hanabi_player import HanabiPlayer

#To create an AI for Hanabi, make a new class in the ai folder,
#extend HanabiPlayer, and implement do_turn
class Discarder(HanabiPlayer):
    def __init__(self):
        pass

    def do_turn(self, player_index, game_info):
        if game_info["disclosures"] < game.NUM_DISCLOSURES:
            return moves.HanabiDiscardAction(player_index, 0)
        else:
            return moves.HanabiDiscloseRankAction(player_index,
                (player_index + 1) % game_info["num_players"],
                0,
                1)
