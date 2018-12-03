class HanabiDiscard:
    #probably should just be a variable, but I already wrote it /shrug
    def __init__(self):
        self.pile = []

    def add(self, card):
        self.pile.append(card)

    def contains(self, card):
        return card in self.pile

    def discarded(self):
        return self.pile

    def __len__(self):
        return len(self.pile)

    def __str__(self):
        res = ""
        for card in self.pile:
            res += str(card)+" "
        return res.strip()
