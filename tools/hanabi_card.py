from enum import Enum, IntEnum

class HanabiColor(Enum):
    RED = 'R'
    BLUE = 'B'
    GREEN = 'G'
    WHITE = 'W'
    YELLOW = 'Y'
    RAINBOW = '*'

class KnownInfo(IntEnum):
    NONE_KNOWN = 0b00
    RANK_KNOWN = 0b01
    COLOR_KNOWN = 0b10
    FULLY_KNOWN = 0b11

class HanabiCard:
    def __init__(self, color, rank):
        self.known_info = KnownInfo.NONE_KNOWN
        self.color = color
        self.rank = rank
        self.told_color = None

    def known(self):
        UNKNOWN = '?'
        info = {
            KnownInfo.NONE_KNOWN : (UNKNOWN, UNKNOWN),
            KnownInfo.RANK_KNOWN : (UNKNOWN, self.rank),
            KnownInfo.COLOR_KNOWN : (self.told_color, UNKNOWN),
            KnownInfo.FULLY_KNOWN : (self.told_color, self.rank),
        } [self.known_info]
        return "{color}{rank}".format(color = info[0], rank = info[1])

    def disclose_rank(self):
        self.known_info |= KnownInfo.RANK_KNOWN

    def disclose_color(self, color):
        if self.color == color or self.color == HanabiColor.RAINBOW:
            if self.told_color is None:
                self.told_color = color.value
            elif self.told_color != color.value:
                self.told_color = self.color.value
            self.known_info |= KnownInfo.COLOR_KNOWN

    def __str__(self):
        return "{color}{rank}".format(color = self.color.value, rank = self.rank)

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.rank == other.rank and self.color == other.color
        else:
            return False

    def __ne__(self, other):
        return not self.__eq__(other)