#helper methods
def can_discard(game_info):
    return game_info['disclosures'] < 8

#actions
def discard_oldest_first(player_id, game_info):
    if can_discard(game_info):
        return {
            "play_type":"discard",
            "card":0
        }
    else:
        return None
