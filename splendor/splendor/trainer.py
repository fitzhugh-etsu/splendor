import itertools
from .models import Game, Player
from . import search
from . import actions

def head_to_head_champion(mcqueen, mr_the_king, threshold=0.55, game_count=1000, seed=None):
    raise Exception("Implement the H2H champion")
    return mcqueen

def run_episode(agent, seed=None, players=4, mcts_count=12000):
    actions_list = []

    mcts_db = search.create_db()            # initialise search tree
    game = Game.setup_game(seed=seed, players=players)
    player_i = (game.turn % len(game.players))
    passes = 0
    while not Game.over(game):
        if game.turn % len(game.players) == 0:
            if passes == len(game.players):
                print("Passed too many times")
                break

            passes = 0

        action, intent = agent_intent = search.get_agent_intent(
            game, agent,
            simulations=mcts_count, seed=seed)

        actions_list.append(agent_intent)

        # Evaluate
        if intent:
            action = actions.evaluate_player_intent(game, intent)
        else:
            print("PASSES")
            passes += 1

        game = action.game

    if Player.won(game.players[player_i]):
       return zip(actions_list, itertools.repeat(search.WON_SCORE))
    else:
       return zip(actions_list, itertools.repeat(search.LOST_SCORE))

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

        mr_the_king = head_to_head_champion(mcqueen, mr_the_king, threshold=threshold,
                                            game_count=episode_length)  # compare new net with previous net
    return mr_the_king
