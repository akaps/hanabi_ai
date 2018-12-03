class HanabiColor:
    RED = 'R'
    BLUE = 'B'
    GREEN = 'G'
    WHITE = 'W'
    YELLOW = 'Y'
    RAINBOW = '*'

class HanabiCard:
    NONE_KNOWN = 0b00
    RANK_KNOWN = 0b01
    COLOR_KNOWN = 0b10
    FULLY_KNOWN = 0b11

    def __init__(self, color, rank):
        self.known_info = self.NONE_KNOWN
        self.color = color
        self.rank = rank
        self.told_color = None

    def known(self):
        unknown = '?'
        info = {
            self.NONE_KNOWN : (unknown, unknown),
            self.RANK_KNOWN : (unknown, self.rank),
            self.COLOR_KNOWN : (self.told_color, unknown),
            self.FULLY_KNOWN : (self.told_color, self.rank),
        }[self.known_info]
        return "{color}{rank}".format(color=info[0], rank=info[1])

    def disclose_rank(self):
        self.known_info |= self.RANK_KNOWN

    def disclose_color(self, color, is_rainbow_wild=False):
        if self.color == color or (is_rainbow_wild and self.color == HanabiColor.RAINBOW):
            if self.told_color is None:
                self.told_color = color
            elif self.told_color != color:
                self.told_color = self.color
            self.known_info |= self.COLOR_KNOWN
            return True
        return False

    def __str__(self):
        return "{color}{rank}".format(color=self.color, rank=self.rank)

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.rank == other.rank and self.color == other.color
        return False

    def __ne__(self, other):
        return not self.__eq__(other)
