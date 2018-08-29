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

    def known(self):
        UNKNOWN = '?'
        return {
            KnownInfo.NONE_KNOWN : UNKNOWN + UNKNOWN,
            KnownInfo.RANK_KNOWN : UNKNOWN + str(self.rank),
            KnownInfo.COLOR_KNOWN : str(self.color.value) + UNKNOWN,
            KnownInfo.FULLY_KNOWN : str(self),
        } [self.known_info]

    def disclose_rank(self):
        self.known_info |= KnownInfo.RANK_KNOWN

    def disclose_color(self):
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