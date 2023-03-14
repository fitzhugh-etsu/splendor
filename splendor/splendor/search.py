import random
import splendor.io as io
from splendor.models.game import Game
from collections import defaultdict
from typing import NamedTuple
import lmdb

WON_SCORE = 1
LOST_SCORE = -1

class SearchDB(NamedTuple):
    visited: set = set()

    # stores Q values for s,a (as defined in the paper)
    Qsa: dict = defaultdict(lambda: defaultdict(float))
    # Qsa: dict = {}

    # stores # times edge s,a visited
    Nsa: dict = defaultdict(lambda: defaultdict(int))
    # Nsa: dict = {}

    # stores # times s visited
    Ns: dict = defaultdict(lambda: int)
    # Ns: dict = {}

    # stores initial policy, returned by neural net
    position_qualities: dict = {}

    # stores game.ended for board s?
    Ns: dict = defaultdict(lambda: bool),
    # Es: dict = {}

    # stores game.getValidMoves for board s
    Vs: dict = {}

def _search(db, game, agent):
    if Player.won(game):
        return WON_SCORE
    elif Game.over(game):
        return LOST_SCORE

    if game not in db.visited:
        db.visited.add(game)
        agent_intent = agent.evaluate(agent, io.inputs(game))
        db.position_qualities[game] = agent_intent.position_quality
        return agent_intent

    max_u, best_a = -float("inf"), -1

    for action in actions.valid_actions(game)
        u = db.Q[s][a] + c_puct*P[s][a]*sqrt(sum(N[s]))/(1+N[s][a])
        if u>max_u:
            max_u = u
            best_a = a
    a = best_a

    sp = game.nextState(s, a)
    v = search(sp, game, nnet)

    Q[s][a] = (N[s][a]*Q[s][a] + v)/(N[s][a]+1)
    N[s][a] += 1
    return -v


        if s not in self.Es:
            self.Es[s] = self.game.getGameEnded(canonicalBoard, 1)
        if self.Es[s] != 0:
            # terminal node
            return -self.Es[s]

        if s not in self.Ps:
            # leaf node
            self.Ps[s], v = self.nnet.predict(canonicalBoard)
            valids = self.game.getValidMoves(canonicalBoard, 1)
            self.Ps[s] = self.Ps[s] * valids  # masking invalid moves
            sum_Ps_s = np.sum(self.Ps[s])
            if sum_Ps_s > 0:
                self.Ps[s] /= sum_Ps_s  # renormalize
            else:
                # if all valid moves were masked make all valid moves equally probable

                # NB! All valid moves may be masked if either your NNet architecture is insufficient or you've get overfitting or something else.
                # If you have got dozens or hundreds of these messages you should pay attention to your NNet and/or training process.
                log.error("All valid moves were masked, doing a workaround.")
                self.Ps[s] = self.Ps[s] + valids
                self.Ps[s] /= np.sum(self.Ps[s])

            self.Vs[s] = valids
            self.Ns[s] = 0
            return -v

        valids = self.Vs[s]
        cur_best = -float('inf')
        best_act = -1

        # pick the action with the highest upper confidence bound
        for a in range(self.game.getActionSize()):
            if valids[a]:
                if (s, a) in self.Qsa:
                    u = self.Qsa[(s, a)] + self.args.cpuct * self.Ps[s][a] * math.sqrt(self.Ns[s]) / (
                            1 + self.Nsa[(s, a)])
                else:
                    u = self.args.cpuct * self.Ps[s][a] * math.sqrt(self.Ns[s] + EPS)  # Q = 0 ?

                if u > cur_best:
                    cur_best = u
                    best_act = a

        a = best_act
        next_s, next_player = self.game.getNextState(canonicalBoard, 1, a)
        next_s = self.game.getCanonicalForm(next_s, next_player)

        v = self.search(next_s)

        if (s, a) in self.Qsa:
            self.Qsa[(s, a)] = (self.Nsa[(s, a)] * self.Qsa[(s, a)] + v) / (self.Nsa[(s, a)] + 1)
            self.Nsa[(s, a)] += 1

        else:
            self.Qsa[(s, a)] = v
            self.Nsa[(s, a)] = 1

        self.Ns[s] += 1
        return -v


def search(game, agent, db=None):
    if not db:
        db = SearchDB()
    return _search(db, game, agent)

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
