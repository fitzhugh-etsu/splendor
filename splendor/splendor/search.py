import random
from collections import defaultdict
from math import log, sqrt

import lmdb
from dotted_dict import DottedDict

import splendor.actions as actions
import splendor.io as io
from splendor.models.game import Game, Player

from .models.actions import PerformedAction, pass_intent, pass_turn

WON_SCORE = 1
LOST_SCORE = -1

class MCTSDB():
    def __init__(self):
        self.db = defaultdict(lambda: DottedDict(dict(count=0, action=None, reward=0, intent=None, children=list())))

    def visited(self, game):
        return game in self.db

    def visited_children(self, game):
        for child in self.get_children(game):
            if self.visited(child.action.game):
                yield (self.get_reward(child.action.game), child.action)

    def visit(self, game, game_actions, probabilities):
        self.db[game].children = [
            DottedDict(action=a, prob=p) for (a, p) in
            zip(game_actions, probabilities)
            if a]

    def set_reward(self, game, reward):
        self.db[game].reward = reward

    def set_intent(self, game, intent):
        self.db[game].intent = intent

    def get_intent(self, game):
        if game in self.db:
            return self.db[game].intent
        else:
            return 0

    def get_reward(self, game):
        if game in self.db:
            return self.db[game].reward
        else:
            return 0

    def incr_count(self, game):
        if game in self.db:
            self.db[game].count += 1
        else:
            raise Exception("Can't incr if not visited")

    def get_count(self, game):
        if game in self.db:
            return self.db[game].count
        else:
            return 0

    def get_children(self, game):
        if game in self.db:
            return self.db[game].children
        else:
            return []

def _mcts(db, game, player_i, agent, cpuct=1.0, seed=None):
    is_player_active = player_i == (game.turn % len(game.players))

    # If we hit a terminal node
    #  either we won
    if Player.won(game.players[player_i]):
        return WON_SCORE
    # Or someone else did (we lost!)
    elif Game.over(game):
        return LOST_SCORE

    if not db.visited(game):
        intent = agent.evaluate(io.inputs(game))
        # Get a list of valid moves and slap them into the
        # Chidren, with  probabilities included
        db.visit(
            game,
            game_actions=actions.valid_actions(game, yield_invalid=True),
            probabilities=intent.action_probabilities)

        # Set the position_quality of this board
        # It is from the player_i's perspective, so
        # if it's the other player, then we want to
        #       inverse the quality
        if not is_player_active:
            db.set_reward(game, -1 * intent.position_quality)
        else:
            db.set_reward(game, intent.position_quality)

        # Return this position value - since we just found this node

        db.set_intent(game, intent)

        return db.get_reward(game)
    else:
        def u(child):
            count = db.get_count(child.action.game)
            reward = db.get_reward(child.action.game)
            parent_count = db.get_count(game)

            # Pull action probability from the intent
            return ((reward / (1 + count)) +
                    cpuct * child.prob * sqrt(log(1 + parent_count) /
                                              (1 + count)))

        # Look at children
        if children := db.get_children(game):
            scored_values = [(i, u(child)) for i, child in enumerate(children)]
            max_score = max([v for (_, v) in scored_values])

            best_i = random.Random(seed).choice([i for (i, v)
                                                 in scored_values
                                                 if v >= max_score])
            best = children[best_i]

            # Search on that action.
            child_reward = _mcts(db,
                                 best.action.game,
                                 player_i,
                                 agent,
                                 cpuct=cpuct,
                                 seed=seed)

            # Normalize it.
            new_reward = ((db.get_count(game) * db.get_reward(game)) + child_reward) / (db.get_count(game) + 1)
            db.set_reward(game, new_reward)

            db.incr_count(game)

            return new_reward
        else:
            # No possible moves.
            db.incr_count(game)
            db.set_reward(game, 0)
            return 0


def monte_carlo_tree_search(game, agent, db=None, cpuct=1.0, seed=None):
    if not db:
        db = MCTSDB()
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
    db = MCTSDB()
    player_i = (game.turn % len(game.players))

    def visited(game):
        return game in db

    for i in range(simulations):
        _mcts(db, game, player_i, agent, seed=seed)

    # Now that we've filled in the DB with details, we can analyze it

    # Find possible actions (only visited children)
    possible_child_actions = list(db.visited_children(game))

    if possible_child_actions:
        # Find out the max reward score
        max_reward = max([a[0] for a in possible_child_actions])
        # which are possible
        max_value_actions = [a[1] for a in possible_child_actions if a[0] >= max_reward]

        if not max_value_actions:
            import pudb; pudb.set_trace()
        best_action = random.Random(seed).choice(max_value_actions)

        # Want to return a list of probabilities for actions
        return best_action, db.get_intent(best_action.game)
    else:
        best_action = PerformedAction(
            action=None,
            game=pass_turn(game))

        return (best_action, pass_intent())
