import random

from . import actions, io
from .models import Game, Player


def gem_return_action(game, affinity):
    more = True

    while more:
        action_list = list(actions.valid_payback_actions_for_last_player(game, yield_invalid=True))
        more = any(action_list)

        if more:
            action = random.choices(
                action_list,
                weights=[(action_list[i] and affinity[i]) or 0
                         for i in
                         range(len(action_list))])
            return action[0]
    return None

def noble_accept_action(game, affinity):
    more = True

    while more:
        action_list = list(actions.valid_nobles_for_last_player(game, yield_invalid=True))
        more = any(action_list)

        if more:
            action = random.choices(
                action_list,
                weights=[(action_list[i] and affinity[i]) or 0
                         for i in
                         range(len(action_list))])
            return action[0]
    return None

def winner(game):
    winners = []
    for (i, player) in enumerate(game.players):
        if Player.won(player):
            # The tiebreakers are (points, purch
            winners.append((i,
                            # Most points
                            Player.points(player),
                            # Least purchased
                            -1 * len(player.purchased)))
    if winners:
        winners.sort(key=lambda x: x[1:])
        return winners[0]
    else:
        return None

def play_game(networks, seed=None):
    # each_network indicates a player.
    game = Game.setup_game(players=len(networks), seed=seed)
    while not winner(game):
        for player_i, network in enumerate(networks):

            possible_outputs = io.outputs(game)

            (resource_affinity,
             noble_affinity,
             action_probabilities) = network.evaluate(
                io.inputs(game),
                possible_outputs)

            # Pick action
            action_p = [(possible_outputs[i] and action_probabilities[i]) or 0
                        for i in
                        range(len(action_probabilities))]

            if any(action_p):
                action = random.choices(
                    possible_outputs,
                    weights=action_p,
                    k=1)[0]

                print(f"Player {player_i} chose {action.action}")
                game = action.game

                # Now check for payback gems
                while (gem_action := gem_return_action(game, resource_affinity)):
                    print(f"Player {player_i} decided {gem_action.action}")
                    game = gem_action.game

                # Now check for noble visits
                if (noble_action := noble_accept_action(game, noble_affinity)):
                    print(f"Player {player_i} decided {noble_action.action}")
                    game = noble_action.game

            else:
                print(f"Player {player_i} PASSES")

    winner_i = winner(game)
    return (winner_i,
            [Player.points(p) for p in game.players])

if __name__ == "__main__":
    from .networks import random as random_network

    print(play_game([random_network] * 4, seed=1))
