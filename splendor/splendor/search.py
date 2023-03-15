import random
import splendor.io as io
from splendor.models.game import Game
from collections import defaultdict
from typing import NamedTuple
import lmdb
import splendor.actions as actions

WON_SCORE = 1
LOST_SCORE = -1

class MCTSDB(NamedTuple):
    visited: set = set()

    # stores state_qualities for that state
    position_qualities: dict = defaultdict(lambda: float)

    # How many times has a state been visited?
    visits: dict = defaultdict(lambda: 0)

    valid_moves_from_state: dict = {}

    # stores Q values for s,a (as defined in the paper)
    Qsa: dict = defaultdict(lambda: defaultdict(float))
    # Qsa: dict = {}

    # stores # times edge s,a visited
    Nsa: dict = defaultdict(lambda: defaultdict(int))
    # Nsa: dict = {}

    # stores # times s visited
    Ns: dict = defaultdict(lambda: int)
    # Ns: dict = {}

    # stores game.ended for board s?
    Es: dict = defaultdict(lambda: int),

    # stores game.getValidMoves for board s
    Vs: dict = {}

def _mcts(db, game, player_i, agent):
    is_player_active = player_i == (game.turn % len(game.players))

    # If we hit a terminal node
    #  either we won
    if Player.won(game.players[player_i]):
        return WON_SCORE
    # Or someone else did (we lost!)
    elif Game.over(game):
        return LOST_SCORE

    if game not in db.position_qualities:
        intent = agent.evaluate(game)
        # Set the position_quality of this board
        # It is from the player_i's perspective, so
        # if it's the other player, then we want to
        #       inverse the quality
        if is_player_active:
            db.position_qualities[game] = intent.position_quality
        else:
            db.position_qualities[game] = -intent.position_quality

        # Get a list of valid moves
        valid_moves = list(actions.valid_actions(game))
        db.valid_moves_from_state[game] = valid_moves

        db.visits[game] += 1
#
#
#   if game not in db.visited:
#       db.visited.add(game)
#       agent_intent = agent.evaluate(agent, io.inputs(game))
#       db.position_qualities[game] = agent_intent.position_quality
#       return agent_intent
#
#   max_u, best_a = -float("inf"), -1
#
#   for action in actions.valid_actions(game):
#       u = db.Q[s][a] + c_puct*P[s][a]*sqrt(sum(N[s]))/(1+N[s][a])
#       if u>max_u:
#           max_u = u
#           best_a = a
#   a = best_a
#
#   sp = game.nextState(s, a)
#   v = search(sp, game, nnet)
#
#   Q[s][a] = (N[s][a]*Q[s][a] + v)/(N[s][a]+1)
#   N[s][a] += 1
#   return -v
#
#
#       if s not in self.Es:
#           self.Es[s] = self.game.getGameEnded(canonicalBoard, 1)
#       if self.Es[s] != 0:
#           # terminal node
#           return -self.Es[s]
#
#       if s not in self.Ps:
#           # leaf node
#           self.Ps[s], v = self.nnet.predict(canonicalBoard)
#           valids = self.game.getValidMoves(canonicalBoard, 1)
#           self.Ps[s] = self.Ps[s] * valids  # masking invalid moves
#           sum_Ps_s = np.sum(self.Ps[s])
#           if sum_Ps_s > 0:
#               self.Ps[s] /= sum_Ps_s  # renormalize
#           else:
#               # if all valid moves were masked make all valid moves equally probable
#
#               # NB! All valid moves may be masked if either your NNet architecture is insufficient or you've get overfitting or something else.
#               # If you have got dozens or hundreds of these messages you should pay attention to your NNet and/or training process.
#               log.error("All valid moves were masked, doing a workaround.")
#               self.Ps[s] = self.Ps[s] + valids
#               self.Ps[s] /= np.sum(self.Ps[s])
#
#           self.Vs[s] = valids
#           self.Ns[s] = 0
#           return -v
#
#       valids = self.Vs[s]
#       cur_best = -float('inf')
#       best_act = -1
#
#       # pick the action with the highest upper confidence bound
#       for a in range(self.game.getActionSize()):
#           if valids[a]:
#               if (s, a) in self.Qsa:
#                   u = self.Qsa[(s, a)] + self.args.cpuct * self.Ps[s][a] * math.sqrt(self.Ns[s]) / (
#                           1 + self.Nsa[(s, a)])
#               else:
#                   u = self.args.cpuct * self.Ps[s][a] * math.sqrt(self.Ns[s] + EPS)  # Q = 0 ?
#
#               if u > cur_best:
#                   cur_best = u
#                   best_act = a
#
#       a = best_act
#       next_s, next_player = self.game.getNextState(canonicalBoard, 1, a)
#       next_s = self.game.getCanonicalForm(next_s, next_player)
#
#       v = self.search(next_s)
#
#       if (s, a) in self.Qsa:
#           self.Qsa[(s, a)] = (self.Nsa[(s, a)] * self.Qsa[(s, a)] + v) / (self.Nsa[(s, a)] + 1)
#           self.Nsa[(s, a)] += 1
#
#       else:
#           self.Qsa[(s, a)] = v
#           self.Nsa[(s, a)] = 1
#
#       self.Ns[s] += 1
#       return -v


def monte_carlo_tree_search(game, agent, db=None):
    if not db:
        db = SearchDB()
    return _mcts(db, game, agent)

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
    db = SearchDB()

    for i in range(simulations):
        search(starting_board, agent, db=db)

    # Now that we've filled in the DB with details, we can analyze it

    # Want to return a list of probabilities for actions

    # This will take the starting board and
    #   pull out a list of all the # actions
    #   filling in 0s for any missing action
    counts = [(i, db.Nsa[starting_board][a])
              if s in db.Nsa and a in db.Nsa[starting_board]
              else 0
              for (i, a) in enumerate(len(io.actions(starting_board)))]

    if temp == 0:
        max_count = max(db.Nsa[starting_board])

        # Find the best intent index?
        best_intent_i = random.Random(seed).choice(
            [i for
             (i, count) in enumerate(db.Nsa[starting_board])
             if count == max_count
            ])

        # MAKE IT A LIST
        # Find the intent with the highest counts
        return probs
    else:
        counts = [x ** (1. / temp) for x in counts]
        counts_sum = float(sum(counts))
        probs = [x / counts_sum for x in counts]
        return probs
