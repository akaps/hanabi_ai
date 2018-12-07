import random
import hanabi_ai.model.moves as moves

def color(card):
    return card[0]

def rank(card):
    return (int)(card[1])

#actions
def discard_oldest_first(player_id, game_info):
    if game_info.can_discard():
        return moves.HanabiDiscardAction(
            player_id,
            0)
    return None

def play_safe_card(player_id, game_info):
    hand = game_info.player_hand(player_id)
    index = 0
    for card in hand:
        if '?' not in card and game_info.is_safe(card):
            return moves.HanabiPlayAction(
                player_id,
                index)
        index += 1
    return None

def tell_randomly(player_id, game_info, seed=None):
    if game_info.can_disclose():
        next_id = game_info.next_player(player_id)
        random.seed(seed)
        choice = random.choice(game_info.hands[next_id])
        if random.random() < .5:
            return moves.HanabiDiscloseRankAction(
                player_id,
                next_id,
                rank(choice))
        return moves.HanabiDiscloseColorAction(
            player_id,
            next_id,
            color(choice))
    return None

def discard_randomly(player_id, game_info, seed=None):
    if game_info.can_discard():
        random.seed(seed)
        return moves.HanabiDiscardAction(
            player_id,
            random.randint(0, game_info.cards_in_hand() - 1))
    return None

def tell_unknown(player_id, game_info, seed=None):
    if game_info.can_disclose():
        next_player = game_info.next_player(player_id)
        random.seed(seed)
        res = []
        for card_index in range(0, game_info.cards_in_hand()):
            card_color = game_info.known_info[next_player][card_index][0]
            if card_color == '?':
                res.append(moves.HanabiDiscloseColorAction(
                    player_id,
                    next_player,
                    color(game_info.hands[next_player][card_index])))
            card_rank = game_info.known_info[next_player][card_index][1]
            if card_rank == '?':
                res.append(moves.HanabiDiscloseRankAction(
                    player_id,
                    next_player,
                    rank(game_info.hands[next_player][card_index])))
        if res:
            return random.choice(res)
    return None

def tell_playable(player_id, game_info, seed=None):
    if game_info.can_disclose():
        next_player = game_info.next_player(player_id)
        random.seed(seed)
        res = []
        for card_index in range(0, game_info.cards_in_hand()):
            card = game_info.hands[next_player][card_index]
            if game_info.is_safe(card):
                card_info = game_info.known_info[next_player][card_index]
                if card_info[0] == '?':
                    res.append(moves.HanabiDiscloseColorAction(
                        player_id,
                        next_player,
                        color(card)
                    ))
                if card_info[1] == '?':
                    res.append(moves.HanabiDiscloseRankAction(
                        player_id,
                        next_player,
                        rank(card)
                    ))
        if res:
            return random.choice(res)
    return None
