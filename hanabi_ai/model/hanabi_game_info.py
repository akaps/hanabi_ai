class GameInfo(object):
    def __init__(self,
                 score=0,
                 deck_size=0,
                 discarded=None,
                 disclosures=0,
                 mistakes_left=0,
                 num_players=0,
                 hands=None,
                 known_info=None,
                 scored_cards=None,
                 history=None):
        self.score = score
        self.deck_size = deck_size
        self.discarded = discarded
        self.disclosures = disclosures
        self.mistakes_left = mistakes_left
        self.num_players = num_players
        self.hands = hands
        self.known_info = known_info
        self.scored_cards = scored_cards
        self.history = history

    #helper methods
    def can_disclose(self):
        return self.disclosures > 0

    def can_discard(self):
        return self.disclosures < 8

    def is_safe(self, card):
        [color, rank] = list(card)
        return self.scored_cards[color] + 1 == (int)(rank)

    def next_player(self, player_id):
        return (player_id + 1) % self.num_players

    def cards_in_hand(self):
        return len(self.hands[0])

    def player_hand(self, player_id):
        return self.known_info[player_id]
