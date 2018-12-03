class HanabiPlayer:
    def do_turn(self, player_index, game_info):
        """
        evaluates and returns the next move to make for Hanabi

        @param self: class reference variable
        @param player_index: referring index for the player the AI is playing as.
            Locate player info using the index
        @param game_info: object of all relevant info for the current state of Hanabi.
            The fields are:
            score: current game score
            deck_size: how many cards are left in the deck
            discarded: list of discarded cards
            disclosures: number of times information can be given
            mistakes_left: how many more mistakes can be made
            num_players: number of players in the game
            hands: for player_index, all visible and known cards
                (you can't see your own cards)
            known_info: all given information about each hand, so you can avoid
                telling the same info
            scored_cards: dictionary of highest scored card per pile. Uses first letter
                of a color as key (i.e. "R")
            history: list of moves objects made throughout the game. All are defined
                in hanabi_moves.py

        @return an Action of the command to do. The Actions are
            HanabiPlayAction: plays a card
            HanabiDiscardAction: discards a card
            HanabiDiscloseColorAction: discloses a color to a specified player
            HanabiDiscloseRankAction: discloses a rank to a specified player
        """
