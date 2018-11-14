class GameInfo:
    def __init__(self):
        self.score = 0
        self.deck_size = 0
        self.discarded = []
        self.disclosures = 0
        self.mistakes_left = 0
        self.num_players = 0
        self.hands = []
        self.known_info = []
        self.scored_cards = {}
        self.history = []

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
