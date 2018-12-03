import random
import hanabi_ai.model.hanabi_moves as moves

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
                (int)(choice[1]))
        return moves.HanabiDiscloseColorAction(
            player_id,
            next_id,
            choice[0])
    return None

def discard_randomly(player_id, game_info, seed=None):
    if game_info.can_discard():
        random.seed(seed)
        return moves.HanabiDiscardAction(
            player_id,
            random.randint(0, game_info.cards_in_hand() - 1))
    return None
