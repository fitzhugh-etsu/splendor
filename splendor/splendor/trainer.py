import itertools
import sys

import splendor.io as io

from . import actions, search
from .models import Game, Player


def head_to_head_champion(
    mcqueen, mr_the_king,
    players=4, threshold=0.55,
        mcts_count=100,
        game_count=50, seed=None):

    player_i = 0
    mcqueen_wins = 0

    for game_i in range(game_count):
        game = Game.setup_game(seed=seed, players=players)
        passes = 0

        while not Game.over(game):
            if game.turn % players == 0:
                if passes == players:
                    print("Passed too many times - stalemate")
                    break

                passes = 0

            player_agent = None

            # Switch agent depending on player
            # one mcqueen vs X mr_the_kings
            if game.turn % players == player_i:
                player_agent = mcqueen
            else:
                player_agent = mr_the_king

            action, intent = search.get_agent_intent(
                game,
                player_agent,
                simulations=mcts_count,
                seed=seed)

            if action.action is None:
                print("P", end='')
                passes += 1
            else:
                print(".", end='')
            sys.stdout.flush()

            action = actions.evaluate_player_intent(game, intent)

            # New turn
            game = action.game

        # Game over
        if Player.won(game.players[player_i]):
            mcqueen_wins += 1
        else:
            pass

    if (mcqueen_wins / game_count) >= threshold:
        print("Have a new champion!")
        return mcqueen
    else:
        return mr_the_king

def run_episode(agent, seed=None, players=4, mcts_count=12000):
    actions_list = []

    game = Game.setup_game(seed=seed, players=players)
    player_i = (game.turn % len(game.players))
    passes = 0
    while not Game.over(game):
        print('.', end='')
        sys.stdout.flush()

        if game.turn % len(game.players) == 0:
            if passes == len(game.players):
                print("Passed too many times")
                break

            passes = 0

        action, intent = agent_intent = search.get_agent_intent(
            game, agent,
            simulations=mcts_count, seed=seed)

        actions_list.append((
            io.inputs(action.game),
            intent.to_tuple()))

        if action.action is None:
            print("PASSES")
            passes += 1

        # Evaluate
        action = actions.evaluate_player_intent(game, intent)

        game = action.game

    if Player.won(game.players[player_i]):
        return map(lambda r: (r[0], r[1], search.WON_SCORE), actions_list)
    else:
        return map(lambda r: (r[0], r[1], search.LOST_SCORE), actions_list)

def training_loop(mr_the_king, seed=None, players=4,
                  episodes=10,
                  episode_length=100,
                  mcts_count=12000, threshold=0.55):

    actions_list = []

    for e in range(episodes):
        for ei in range(episode_length):
            print(f"Episode: {e}:{ei}")
            actions_list.extend(run_episode(mr_the_king, players=players, seed=seed, mcts_count=mcts_count))   # collect examples from this game

        mcqueen = mr_the_king.train_new(actions_list)

        # Who is the new mr_the_king?
        mr_the_king = head_to_head_champion(
            mcqueen,
            mr_the_king,
            players=players,
            threshold=threshold,
            mcts_count=mcts_count,
            game_count=episode_length)  # compare new net with previous net

    return mr_the_king
