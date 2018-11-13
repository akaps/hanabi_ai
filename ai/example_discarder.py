import tools.hanabi_table as game
from hanabi_player import HanabiPlayer

#To create an AI for Hanabi, make a new class in the ai folder,
#extend HanabiPlayer, and implement do_turn
class Discarder(HanabiPlayer):
    def __init__(self):
        pass

    def do_turn(self, player_index, game_info):
        if game_info.disclosures < game.NUM_DISCLOSURES:
            return {
                "play_type":"discard",
                "card":0
                }
        else:
            return {
                "play_type":"disclose",
                "player":(player_index + 1) % game_info.num_players,
                "disclose_type":"rank",
                "rank":1
            }
