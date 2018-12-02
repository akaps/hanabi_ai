import random
import enum
from hanabi_ai.model.hanabi_card import HanabiCard, HanabiColor

class HanabiVariant(enum.IntEnum):
    basic = 0
    sixth_suit = 1
    sixth_suit_hard = 2
    rainbow_wild = 3

class HanabiDeck(object):

    def __init__(self, seed, variant=HanabiVariant.basic):
        colors = [HanabiColor.BLUE,
                  HanabiColor.GREEN,
                  HanabiColor.RED,
                  HanabiColor.YELLOW,
                  HanabiColor.WHITE]
        self.deck = [HanabiCard(color, 1) for _ in range(0, 3) for color in colors]
        self.deck.extend([HanabiCard(color, rank)
                          for _ in range(0, 2)
                          for rank in range(2, 5)
                          for color in colors])
        self.deck.extend([HanabiCard(color, 5) for color in colors])
        self.add_rainbow(variant)
        random.seed(seed)
        random.shuffle(self.deck)

    def add_rainbow(self, variant):
        if variant != HanabiVariant.basic:
            num_ones = {
                HanabiVariant.sixth_suit : 3,
                HanabiVariant.sixth_suit_hard : 1,
                HanabiVariant.rainbow_wild : 3
            }[variant]
            num_cards = {
                HanabiVariant.sixth_suit : 2,
                HanabiVariant.sixth_suit_hard : 1,
                HanabiVariant.rainbow_wild : 2
            }[variant]
            self.deck.extend([HanabiCard(HanabiColor.RAINBOW, 1)
                              for _ in range(0, num_ones)])
            self.deck.extend([HanabiCard(HanabiColor.RAINBOW, rank)
                              for _ in range(0, num_cards)
                              for rank in range(2, 5)])
            self.deck.append(HanabiCard(HanabiColor.RAINBOW, 5))

    def is_empty(self):
        return len(self.deck) == 0

    def draw_card(self):
        return self.deck.pop(0)

    def __len__(self):
        return len(self.deck)

    def __str__(self):
        return "Cards remaining: {cards}".format(cards=len(self))
