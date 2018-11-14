class GameInfo:
    def __init__(self,
        score = 0,
        deck_size = 0,
        discarded = [],
        disclosures = 0,
        mistakes_left = 0,
        num_players = 0,
        hands = [],
        known_info = [],
        scored_cards = [],
        history = []):
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
