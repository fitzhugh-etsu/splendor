from itertools import chain, zip_longest
from typing import NamedTuple

from . import actions
from .models import Bank, Card, Game, Noble, Player



def inputs(game):
    """ These are the inputs to a NN.
      constant size, no matter how many players there are.
    """
    inputs = []

    #  table_bank: Bank = Bank()
    inputs.extend(Bank.to_inputs(game.bank))

    # NOBLES
    #  nobles_left: int = 0
    inputs.append(len(game.nobles_deck))

    #  noble_0: Noble = Noble()
    #  noble_1: Noble = Noble()
    #  noble_2: Noble = Noble()
    #  noble_3: Noble = Noble()
    #  noble_4: Noble = Noble()
    visible = Noble.number_visible(game)
    for (i, noble) in zip_longest(
            range(5),
            game.nobles_deck[0:visible],
            fillvalue=Noble()):
        inputs.extend(Noble.to_inputs(noble))

    # Tier cards
    for tier in range(3):
        #  tier_X_left: int = 0
        inputs.append(len(game.decks[tier]))
        #  tier cards 0 - 3
        for (i, card) in zip_longest(
                range(4),
                game.decks[tier][0:4],
                fillvalue=Card()):
            inputs.extend(Card.to_inputs(card))

    #  current_player: int = 3
    player_i = game.turn % len(game.players)
    inputs.append(player_i)

    for (i, player) in zip_longest(
            range(4),
            game.players[0:4],
            fillvalue=Player()):
        inputs.extend(Player.to_inputs(player, is_current_player=(i == player_i)))

    return inputs

def outputs(game):
    # These are the outputs from the NN.
    # A list of outputs from the NN maps to these actions.
    # The list is constant, so invalid actions are None. Valid ones give a PerformedAction
    return list(actions.valid_actions(game, yield_invalid=True))

if __name__ == "__main__":
    print(inputs(Game.setup_game()))
    print(list(outputs(Game.setup_game())))
