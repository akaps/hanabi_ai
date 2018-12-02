from hanabi_card import HanabiCard

class HanabiHand(object):
    def __init__(self):
        self.hand = []

    def add(self, card):
        self.hand.append(card)

    def show_cards(self, isOwned):
        res = []
        for card in self.hand:
            if (isOwned):
                res.append(card.known())
            else:
                res.append(str(card))
        return res

    def card_at(self, index):
        return self.hand[index]

    def remove_card_at(self, index):
        return self.hand.pop(index)

    def disclose_rank(self, rank):
        for card in self.hand:
            if card.rank == rank:
                card.disclose_rank()

    def disclose_color(self, color, is_rainbow_wild=False):
        for card in self.hand:
            card.disclose_color(color, is_rainbow_wild)

    def pop(self, index):
        return self.hand.pop(index)

    def __len__(self):
        return len(self.hand)
