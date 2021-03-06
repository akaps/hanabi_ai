import hanabi_ai.model.table as game
import hanabi_ai.model.moves as moves
from hanabi_ai.players.player import HanabiPlayer

#To create an AI for Hanabi, make a new class in the ai folder,
#extend HanabiPlayer, and implement do_turn
class Discarder(HanabiPlayer):
    def __init__(self):
        pass

    def do_turn(self, player_index, game_info):
        if game_info.disclosures < game.NUM_DISCLOSURES:
            return moves.HanabiDiscardAction(player_index, 0)
        return moves.HanabiDiscloseRankAction(player_index,
                                              game_info.next_player(player_index),
                                              1)
