#To create an AI for Hanabi, make a new class in the ai folder and implement do_turn
class Discarder:
    def __init__(self):
        pass

    """
    evaluates and returns the next move to make for Hanabi

    @param self: class reference variable
    @param player_index: referring index for the player the AI is playing as. Locate player info using the index
    @param game_info: dictionary of all relevant info for the current state of Hanabi. The keys are:
        "score": current game score
        "deck_size": how many cards are left in the deck
        "discarded": list of discarded cards
        "disclosures": number of times information can be given
        "mistakes_left": how many more mistakes can be made
        "num_players": number of players in the game
        "hands": for player_index, all visible and known cards (you can't see your own cards)
        "known_info": all given information about each hand, so you can avoid telling the same info
        "scored_cards": dictionary of highest scored card per pile. Uses first letter of a color as key (i.e. "R")

    @return a dictionary of the command to do. Uses the following formatting:
        {'play_type':'play', 'card':<number>}
        {'play_type':'discard', 'card':<number>}
        {'play_type':'disclose', 'disclose_type':'color, 'color':<color>}
        {'play_type':'disclose', 'disclose_type':'rank, 'rank':<number>}
    """
    def do_turn(self, player_index, game_info):
        return {
            "move":"discard",
            "card":0
            }