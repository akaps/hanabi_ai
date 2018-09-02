from hanabi_card import HanabiCard, HanabiColor
import random

class HanabiDeck:

    def __init__(self, seed, variant = 0):
        colors = [HanabiColor.BLUE, HanabiColor.GREEN, HanabiColor.RED, HanabiColor.YELLOW, HanabiColor.WHITE]
        self.deck = [HanabiCard(color, 1) for _ in range (0,3) for color in colors]
        self.deck.extend([HanabiCard(color, rank) for _ in range (0,2) for rank in range(2, 5) for color in colors])
        self.deck.extend([HanabiCard(color, 5) for color in colors])
        self.add_rainbow(variant)
        random.seed(seed)
        random.shuffle(self.deck)

    def add_rainbow(self, variant):
        if variant > 0:
            num_ones = {
                1 : 3,
                2 : 1,
                3 : 3 
            } [variant]
            num_cards = {
                1 : 2,
                2 : 1,
                3 : 2
            } [variant]
            self.deck.extend([HanabiCard(HanabiColor.RAINBOW, 1) for _ in range (0, num_ones)])
            self.deck.extend([HanabiCard(HanabiColor.RAINBOW, rank) for _ in range (0, num_cards) for rank in range(2, 5)])
            self.deck.append(HanabiCard(HanabiColor.RAINBOW, 5))


    def is_empty(self):
        return len(self.deck) == 0

    def draw_card(self):
        return self.deck.pop(0)

    def __len__(self):
        return len(self.deck)
        
    def __str__(self):
        return "Cards remaining: {cards}".format(cards = len(self))