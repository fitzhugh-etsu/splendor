from dotted_dict import DottedDict
from math import log, sqrt
import random
import splendor.io as io
from splendor.models.game import Game, Player
from collections import defaultdict
from typing import NamedTuple
import lmdb
import splendor.actions as actions

WON_SCORE = 1
LOST_SCORE = -1

def _normalize(thelist):
    total = sum(thelist)
    return [ i / total for i in thelist]

def _mcts(db, game, player_i, agent, cpuct=1.0):
    is_player_active = player_i == (game.turn % len(game.players))

    # If we hit a terminal node
    #  either we won
    if Player.won(game.players[player_i]):
        print("WON!")
        return WON_SCORE
    # Or someone else did (we lost!)
    elif Game.over(game):
        return LOST_SCORE

    if game not in db:
        intent = agent.evaluate(game)
        # Get a list of valid moves and slap them into the
        # Chidren, with  probabilities included
        db[game].children = [DottedDict(action=a, prob=p) for (a, p) in
             zip(actions.valid_actions(game, yield_invalid=True),
                intent.action_probabilities)
             if a]

        # Set the position_quality of this board
        # It is from the player_i's perspective, so
        # if it's the other player, then we want to
        #       inverse the quality
        if not is_player_active:
            db[game].reward = -1 * intent.position_quality
        else:
            db[game].reward = intent.position_quality

        # Return this position value - since we just found this node
        db[game].intent = intent
        return db[game].reward
    else:
        cur_best = -float('inf')
        best_act = -1

        def u(child):
            performed_action = child.action
            if performed_action.game in db:
                option = db[performed_action.game]
            else:
                option = DottedDict(dict(count=0, reward=0))
            # Pull action probability from the intent
            return ((option.reward / (1 + option.count)) +
                    cpuct * child.prob * sqrt(log(1 + db[game].count) / (1 + option.count)))

        # Look at children
        best = max(db[game].children, key=u)

        # Search on that action.
        child_reward = _mcts(db, best.action.game, player_i, agent, cpuct=cpuct)

        # ?? Q[s][a] = (N[s][a]*Q[s][a] + v)/(N[s][a]+1)
        db[game].reward += child_reward
        db[game].count += 1

        return child_reward

def create_db():
    return defaultdict(lambda: DottedDict(dict(count=0, action=None, reward=0, intent=None, children=list())))

def monte_carlo_tree_search(game, player_i, agent, db=None, cpuct=1.0):
    if not db:
        db = create_db()
    return _mcts(db, game, player_i, agent, cpuct=cpuct)

def get_agent_intent(
    starting_board,
    agent,
    temp=1,
    simulations=500,
        seed=None):
    """
    This function performs numMCTSSims simulations of MCTS starting from
    canonicalBoard.
    Returns:
        probs: a policy vector where the probability of the ith intent is
                proportional to Nsa[(s,a)]**(1./temp)
    """
    db = create_db()
    player_i = (starting_board.turn % len(starting_board.players))

    for i in range(simulations):
        _mcts(db, starting_board, player_i, agent)

    # Now that we've filled in the DB with details, we can analyze it
    best_action, db_record = max([(c.action, db[c.action.game]) for c
                                  in db[starting_board].children], key=lambda r: r[1].reward)
    # Want to return a list of probabilities for actions

    return best_action, db_record.intent
