class GameInfo:
    def __init__(self):
        self.score = 0
        self.deck_size = 0
        self.discarded = None
        self.disclosures = 0
        self.mistakes_left = 0
        self.num_players = 0
        self.hands = None
        self.known_info = None
        self.scored_cards = None
        self.history = None

    #helper methods
    def can_disclose(self):
        return self.disclosures > 0

    def can_discard(self):
        return self.disclosures < 8

    def is_safe(self, card):
        scored = self.scored_cards
        for key in scored:
            if card[0] == key and (int)(card[1]) == scored[key] + 1:
                return True
        return False

    def next_player(self, player_id):
        return (player_id + 1) % self.num_players
