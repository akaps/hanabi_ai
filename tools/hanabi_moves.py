class HanabiCardAction(object):
    def __init__(self, player_id, card):
        self.player_id = player_id
        self.card = card

    def __str__(self):
        return "Player {id} {action} {card}".format(id = self.player_id, action = self.action(), card = str(self.card))

    @classmethod
    def action(self):
        return "N/A"

class HanabiPlayAction(HanabiCardAction):
    
    def __init__(self, player_id, card):
        super(HanabiPlayAction, self).__init__(player_id, card)

    @classmethod
    def parse_move(self, move):
        pass

    @classmethod
    def action(self):
        return "played"

    @staticmethod
    def can_parse_move(move):
        return all(key in move for key in ("play_type", "card")) and \
            move["play_type"] is "play" 

class HanabiDiscardAction(HanabiCardAction):
    def __init__(self, player_id, card):
        super(HanabiDiscardAction, self).__init__(player_id, card)

    @classmethod
    def action(self):
        return "discarded"

    @staticmethod
    def can_parse_move(move):
        return all(key in move for key in ("play_type", "card")) and \
            move["play_type"] is "discard"

class HanabiDiscloseAction(object):
    def __init__(self, player_id, to_whom, count):
        self.player_id = player_id
        self.to_whom = to_whom
        self.count = count

    def __str__(self):
        return "Player {id} told {whom} about {count} {disclosure} in their hand".format( \
            id = self.player_id, \
            whom = self.to_whom, \
            count = self.count, \
            disclosure = self.disclosure())

    def disclosure(self):
        return "N/A"

class HanabiColorDiscloseAction(HanabiDiscloseAction):
    def __init__(self, player_id, to_whom, count, color):
        super(HanabiColorDiscloseAction, self).__init__(player_id, to_whom, count)
        self.color = color
    
    def disclosure(self):
        if self.count == 0:
            return self.color
        else:
            return "{color}s".format(color = self.color)

    @staticmethod
    def can_parse_move(move):
        return all(key in move for key in ("play_type", "player", "disclose_type", "color")) and \
            move["play_type"] is "disclose" and \
            move["disclose_type"] is "color" and \
            move["color"] in "RWBGY*"

class HanabiRankDiscloseAction(HanabiDiscloseAction):
    def __init__(self, player_id, to_whom, count, rank):
        super(HanabiRankDiscloseAction, self).__init__(player_id, to_whom, count)
        self.rank = rank

    def disclosure(self):
        if self.count == 0:
            return self.rank
        else:
            return "{rank}s".format(rank = self.rank)

    @staticmethod
    def can_parse_move(move):
        return all(key in move for key in ("play_type", "player", "disclose_type", "rank")) and \
            move["play_type"] is "disclose" and \
            move["disclose_type"] is "rank" and \
            move["rank"] in range (1,6)
