def remove_card_from_deck(decks, tier, i):
    new_deck = decks[tier][0:i] + decks[tier][i+1:]
    res = decks[0:tier] + (new_deck,) + decks[tier+1:]
    return res

def player_purchase_card(player, card):
    return player._replace(purchased=([card] + player.purchased))

def update_players(players, current_player, new_player):
    return tabletop._replace(
        players=(
            tabletop.players[0:current_player] +
            [new_player] +
            tabletop.players[current_player + 1:]))
