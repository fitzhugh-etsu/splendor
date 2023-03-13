import random

from . import actions, io
from .models import Game, Player


def winner(game, stalemate=False):
    winners = []
    for (i, player) in enumerate(game.players):
        if Player.won(player) or stalemate:
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

def play_game(agents, seed=None):
    # each_agent indicates a player.
    game = Game.setup_game(players=len(agents), seed=seed)
    stalemate = False
    while not winner(game) and not stalemate:
        passed = 0
        for agent in agents:

            possible_outputs = io.outputs(game)

            agent_intent = agent.evaluate(
                agent,
                io.inputs(game),
                possible_outputs)

            action = actions.evaluate_player_intent(game, agent_intent)

            if not action.action:
                passed += 1

            game = action.game

        if passed == len(agents):
            print("Stalemate")
            print(str(game))
            stalemate = True

    winner_i = winner(game, stalemate=stalemate)
    return (winner_i,
            [Player.points(p) for p in game.players])

if __name__ == "__main__":
    from .agents import idiot

    print(play_game([idiot] * 4, seed=1))
