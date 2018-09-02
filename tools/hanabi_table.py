from hanabi_deck import HanabiDeck
from hanabi_discard_pile import HanabiDiscard
from hanabi_hand import HanabiHand
from hanabi_card import HanabiColor

NUM_DISCLOSURES = 8
NUM_MISTAKES = 3

class HanabiTable:
    RAINBOW_IS_WILD = 3


    def __init__(self, num_players, seed, variant):
        self.is_rainbow_wild = variant == self.RAINBOW_IS_WILD
        self.num_players = self.lastTurns = num_players
        self.deck = HanabiDeck(seed, variant)
        self.discard = HanabiDiscard()
        self.disclosures = NUM_DISCLOSURES
        self.mistakes_left = NUM_MISTAKES
        self.hands = [HanabiHand() for _ in range (0, num_players)]
        self.init_hands()
        self.scored_cards = {}
        self.init_tableau(variant)

    def init_hands(self):
        for i in range(0, self.num_players):
            for _ in range(0, self.num_cards(self.num_players)):
                self.hands[i].add(self.deck.draw_card())

    def init_tableau(self, variant):
        self.scored_cards[HanabiColor.RED] = 0
        self.scored_cards[HanabiColor.BLUE] = 0
        self.scored_cards[HanabiColor.GREEN] = 0
        self.scored_cards[HanabiColor.WHITE] = 0
        self.scored_cards[HanabiColor.YELLOW] = 0
        if variant > 0:
            self.scored_cards[HanabiColor.RAINBOW] = 0

    @staticmethod
    def num_cards(num_players):
        return {
            2: 5,
            3: 5,
            4: 4,
            5: 4,
        } [num_players]

    def is_game_over(self):
        return self.mistakes_left == 0 or \
            (len(self.deck) == 0 and self.lastTurns == 0) or \
            self.score() == 25

    def play_card(self, player, card_index):
        card = self.hands[player].pop(card_index)
        if self.can_play(card):
            self.scored_cards[card.color] = card.rank
        else:
            self.discard.add(card)
            self.mistakes_left -= 1
        self.update_hand(player)
        

    def can_play(self, card):
        return self.scored_cards[card.color] == card.rank - 1

    def can_discard(self):
        return self.disclosures < NUM_DISCLOSURES

    def discard_card(self, player, card_index):
        self.disclosures += 1
        card = self.hands[player].pop(card_index)
        self.discard.add(card)
        self.update_hand(player)
    
    def update_hand(self, player):
        if len(self.deck) != 0:
            self.hands[player].add(self.deck.draw_card())
        else:
            self.lastTurns -= 1

    def info_for_player(self, player_index):
        res = {}
        res["score"] = self.score()
        res["deck_size"] = len(self.deck)
        res["discarded"] = self.discard
        res["disclosures"] = self.disclosures
        res["mistakes_left"] = self.mistakes_left
        res["num_players"] = self.num_players
        res["hands"] = self.hands_for_player(player_index)
        res["known_info"] = self.known_cards()
        res["scored_cards"] = self.scored_cards
        return res

    def hands_for_player(self, player_index):
        res = []
        for index in range(0, self.num_players):
            if index == player_index:
                res.append(self.hands[index].show_cards(True))
            else:
                res.append(self.hands[index].show_cards(False))
        return res

    def known_cards(self):
        res = []
        for hand in self.hands:
            res.append(hand.show_cards(True))
        return res

    def can_disclose(self):
        return self.disclosures > 0

    def disclose_rank(self, player_index, rank):
        self.disclosures -= 1
        for card in self.hands[player_index].hand:
            if card.rank == rank:
                card.disclose_rank()

    def disclose_color(self, playerIndex, color):
        self.disclosures -= 1
        for card in self.hands[playerIndex].hand:
            card.disclose_color(color, self.is_rainbow_wild)

    def __str__(self):
        res = "Score: {score}".format(score = self.score())
        res += ", Cards remaining: {cards}".format(cards = len(self.deck))
        res += ", Discarded: {discard}".format(discard = len(self.discard))
        res += ", Disclosures left: {disclosures}".format(disclosures = self.disclosures)
        res += ", Mistakes left: {mistakes}".format(mistakes = self.mistakes_left)
        return res

    def score(self):
        res = 0
        for val in self.scored_cards.values():
            res += val
        return res