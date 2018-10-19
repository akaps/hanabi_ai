class HanabiPlayer:
    def do_turn(self, player_index, game_info):
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
            "history": list of moves objects made throughout the game. All are defined in hanabi_moves.py

        @return a dictionary of the command to do. Uses the following formatting:
            {'play_type':'play', 'card':<number>}
            {'play_type':'discard', 'card':<number>}
            {'play_type':'disclose', 'player':<player_id>, 'disclose_type':'color', 'color':<color>}
            {'play_type':'disclose', 'player':<player_id>, 'disclose_type':'rank', 'rank':<number>}
        """
        pass
        