def valid_actions(tabletop):
    # Find out which player's turn it is
    player_turn = tabletop.turn % len(tabletop.players)
