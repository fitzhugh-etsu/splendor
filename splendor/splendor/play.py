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

def play_game(agent, players=4, seed=None):
    # each_agent indicates a player.
    game = Game.setup_game(players=players, seed=seed)

    stalemate = False

    passed = 0
    while not winner(game) and not stalemate:
        if game.turn % players == 0:
            if passed == players:
                print("Stalemate")
                print(str(game))
                stalemate = True

        possible_outputs = io.outputs(game)

        agent_intent = agent.evaluate(io.inputs(game))

        action = actions.evaluate_player_intent(game, agent_intent, seed=seed)

        if not action.action:
            passed += 1

        game = action.game

    winner_i = winner(game, stalemate=stalemate)
    return (winner_i,
            [Player.points(p) for p in game.players])

if __name__ == "__main__":
    from .agents.idiot import IdiotAgent
    print(play_game(IdiotAgent(seed=1), seed=1))
