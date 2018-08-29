from hanabi_card import HanabiCard, HanabiColor
import random

class HanabiDeck:

    def __init__(self, seed, include_rainbow):
        colors = [HanabiColor.BLUE, HanabiColor.GREEN, HanabiColor.RED, HanabiColor.YELLOW, HanabiColor.WHITE]
        if include_rainbow:
            colors.append(HanabiColor.RAINBOW)
        self.deck = [HanabiCard(color, 1) for _ in range (0,3) for color in colors]
        self.deck.extend([HanabiCard(color, rank) for _ in range (0,2) for rank in range(2, 5) for color in colors])
        self.deck.extend([HanabiCard(color, 5) for color in colors])
        random.seed(seed)
        random.shuffle(self.deck)

    def is_empty(self):
        return len(self.deck) == 0

    def draw_card(self):
        return self.deck.pop(0)

    def __len__(self):
        return len(self.deck)
        
    def __str__(self):
        return "Cards remaining: {cards}".format(cards = len(self))