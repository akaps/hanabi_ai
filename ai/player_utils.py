import random

#helper methods
def can_disclose(game_info):
    return game_info['disclosures'] > 0

def can_discard(game_info):
    return game_info['disclosures'] < 8

def player_hand(player_id, game_info):
    return game_info['hands'][player_id]

def player_info(player_id, game_info):
    return game_info['known_info'][player_id]

def is_safe(card, game_info):
    [color, rank] = list(card)
    scored = game_info['scored_cards']
    return scored[color] + 1 == (int)(rank)

def next_player(player_id, game_info):
    return (player_id + 1) % game_info['num_players']

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
    hand = player_info(player_id, game_info)
    for i in range(len(hand)):
        if '?' not in hand[i] and is_safe(hand[i], game_info):
            return {
                'play_type' : 'play',
                'card' : i
            }
    return None

def tell_randomly(player_id, game_info, seed=None):
    if can_disclose(game_info):
        next = next_player(player_id, game_info)
        result = {
            'play_type' : 'disclose',
            'player' : next
        }
        random.seed(seed)
        choice = random.choice(player_hand(next, game_info))
        if random.random() <.5:
            result['disclose_type'] = 'rank'
            result['rank'] = (int)(choice[1])
        else:
            result['disclose_type'] = 'color'
            result['color'] = choice[0]
        return result
    else:
        return None

def discard_randomly(player_id, game_info, seed=None):
    if can_discard(game_info):
        limit = len(player_hand(player_id, game_info)) - 1
        random.seed(seed)
        return {
            'play_type' : 'discard',
            'card' : random.randint(0, limit)
        }
    else:
        return None
