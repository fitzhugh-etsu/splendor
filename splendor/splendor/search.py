from .models.actions import pass_turn, PerformedAction, pass_intent
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

def _mcts(db, game, player_i, agent, cpuct=1.0, seed=None):
    is_player_active = player_i == (game.turn % len(game.players))

    # If we hit a terminal node
    #  either we won
    if Player.won(game.players[player_i]):
        return WON_SCORE
    # Or someone else did (we lost!)
    elif Game.over(game):
        return LOST_SCORE

    if game not in db:
        intent = agent.evaluate(io.inputs(game))
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
                    cpuct * child.prob * sqrt(log(1 + db[game].count) /
                                              (1 + option.count)))

        # Look at children
        if db[game].children:
            scored_values = [(i, u(child)) for i, child in enumerate(db[game].children)]
            max_score = max([v for (_, v) in scored_values])

            best_i = random.Random(seed).choice([i for (i, v) in scored_values if v >= max_score])
            best = db[game].children[best_i]

            # Search on that action.
            child_reward = _mcts(db, best.action.game, player_i, agent, cpuct=cpuct, seed=seed)

            # Normalize it.
            db[game].reward += ((db[game].count * db[game].reward) + child_reward) / (db[game].count + 1)

            db[game].count += 1

            return child_reward
        else:
            # No possible moves.
            db[game].count += 1
            db[game].reward = 0
            return 0


def create_db():
    return defaultdict(lambda: DottedDict(dict(count=0, action=None, reward=0, intent=None, children=list())))

def monte_carlo_tree_search(game, agent, db=None, cpuct=1.0, seed=None):
    if not db:
        db = create_db()
    player_i = (game.turn % len(game.players))
    return _mcts(db, game, player_i, agent, cpuct=cpuct, seed=seed)

def get_agent_intent(
    game,
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
    player_i = (game.turn % len(game.players))
    def visited(game):
        return game in db

    for i in range(simulations):
        _mcts(db, game, player_i, agent, seed=seed)

    # Now that we've filled in the DB with details, we can analyze it

    # Find possible actions (only visited children)
    possible_child_actions = [
        (c.action, db[c.action.game]) for c
        in db[game].children
        # Needs to have been visited
        if visited(c.action.game)]

    if possible_child_actions:
        # Find out the max reward score
        max_reward = max([a[1].reward for a in possible_child_actions])
        # which are possible
        max_value_actions = [a for a in possible_child_actions if a[1].reward >= max_reward]
        best_action, db_record = random.Random(seed).choice(max_value_actions)

        # Want to return a list of probabilities for actions
        return best_action, db_record.intent
    else:
        best_action =  PerformedAction(
            action=None,
            game=pass_turn(game))

        return (best_action, pass_intent())
