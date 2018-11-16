import abc

class HanabiAction(object):
    __metaclass__ = abc.ABCMeta

    def __init__(self, player_id):
        self.player_id = player_id

    @abc.abstractmethod
    def is_valid(self, game_info):
        pass

    @abc.abstractmethod
    def execute(self, table):
        pass

class HanabiCardAction(HanabiAction):
    def __init__(self, player_id, card):
        super(HanabiCardAction, self).__init__(player_id)
        self.card = card
        self.action_type = ''

    def __str__(self):
        return "Player {id} {action} {card}".format(id = self.player_id, action = self.action_type, card = str(self.card))

class HanabiPlayAction(HanabiCardAction):

    def __init__(self, player_id, card):
        super(HanabiPlayAction, self).__init__(player_id, card)
        self.action_type = 'played'

    def is_valid(self, game_info):
        return True

    def execute(self, table):
        table.play_card(self.player_id, self.card)

class HanabiDiscardAction(HanabiCardAction):
    def __init__(self, player_id, card):
        super(HanabiDiscardAction, self).__init__(player_id, card)
        self.action_type = 'discarded'


    def is_valid(self, game_info):
        return game_info.can_discard()

    def execute(self, table):
        table.discard_card(self.player_id, self.card)

class HanabiDiscloseAction(HanabiAction):
    def __init__(self, player_id, to_whom):
        super(HanabiDiscloseAction, self).__init__(player_id)
        self.to_whom = to_whom
        self.count = 0
        self.disclosure_type = ''

    def pluralize(self, word, count):
        if count <= 1:
            return word
        else:
            return '{word}s'.format(word = word)

    def __str__(self):
        return "Player {id} told {whom} about {count} {disclosure} in their hand".format(
            id = self.player_id,
            whom = self.to_whom,
            count = self.count,
            disclosure = self.disclosure_type)

    def is_valid(self, game_info):
        return game_info.can_disclose()

class HanabiDiscloseColorAction(HanabiDiscloseAction):
    def __init__(self, player_id, to_whom, color):
        super(HanabiDiscloseColorAction, self).__init__(player_id, to_whom)
        self.color = color
        self.disclosure_type = self.pluralize(self.color, self.count)

    def is_valid(self, game_info):
        return (super(HanabiDiscloseColorAction, self).is_valid(game_info) and
            self.color in 'RWBGY*')

    def execute(self, table):
        table.disclose_color(self.player_id, self.to_whom, self.color)

class HanabiDiscloseRankAction(HanabiDiscloseAction):
    def __init__(self, player_id, to_whom, rank):
        super(HanabiDiscloseRankAction, self).__init__(player_id, to_whom)
        self.rank = rank
        self.disclosure_type = self.pluralize(self.rank, self.count)

    def is_valid(self, game_info):
        return (super(HanabiDiscloseRankAction, self).is_valid(game_info) and
            self.rank in range(1,6))

    def execute(self, table):
        table.disclose_rank(self.player_id, self.to_whom, self.rank)
