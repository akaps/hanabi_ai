#helper methods
def can_discard(game_info):
    return game_info['disclosures'] < 8

def player_hand(player_id, game_info):
    return game_info['known_info'][player_id]

def is_safe(card, game_info):
    scored = game_info['scored_cards']
    for key in scored:
        if card[0] == key and (int)(card[1]) == scored[key] + 1:
            return True
    return False

#actions
def discard_oldest_first(player_id, game_info):
    if can_discard(game_info):
        return {
            "play_type" : "discard",
            "card" : 0
        }
    else:
        return None

def play_safe_card(player_id, game_info):
    hand = player_hand(player_id, game_info)
    for i in range(len(hand)):
        if '?' not in hand[i] and is_safe(hand[i], game_info):
            return {
                'play_type' : 'play',
                'card' : i
            }
    return None
