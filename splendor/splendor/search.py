from collections import defaultdict
from typing import NamedTuple
import lmdb

class SearchDB(NamedTuple):
    # stores Q values for s,a (as defined in the paper)
    Qsa: defaultdict(lambda: defaultdict(float)),
    # Qsa: dict = {}

    # stores # times edge s,a visited
    Nsa: defaultdict(lambda: defaultdict(int)),
    # Nsa: dict = {}

    # stores # times s visited
    Ns: defaultdict(lambda: int),
    # Ns: dict = {}

    # stores initial policy, returned by neural net
    Ps: dict = {}
    # stores game.ended for board s?
    Ns: defaultdict(lambda: bool),
    # Es: dict = {}

    # stores game.getValidMoves for board s
    Vs: dict = {}

def search(state, agent, db=None):
    if not db:
        db = SearchDB()
    return _search(db, state, agent)

def search(db, state, agent):
    if game.gameEnded(s): return -game.gameReward(s)

    if s not in visited:
        visited.add(s)
        P[s], v = nnet.predict(s)
        return -v

    max_u, best_a = -float("inf"), -1
    for a in game.getValidActions(s):
        u = Q[s][a] + c_puct*P[s][a]*sqrt(sum(N[s]))/(1+N[s][a])
        if u>max_u:
            max_u = u
            best_a = a
    a = best_a

    sp = game.nextState(s, a)
    v = search(sp, game, nnet)

    Q[s][a] = (N[s][a]*Q[s][a] + v)/(N[s][a]+1)
    N[s][a] += 1
    return -v


def get_agent_intent(starting_board, agent, temp=1, simulations=500):
    """
    This function performs numMCTSSims simulations of MCTS starting from
    canonicalBoard.
    Returns:
        probs: a policy vector where the probability of the ith intent is
                proportional to Nsa[(s,a)]**(1./temp)
    """
    db = SearchDB()

    for i in range(simulations):
        search(db, starting_board, agent)

    # Now that we've filled in the DB, we can analyze it

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
        best_intent_i = random.choice(
            [i for
             (i, count) in enumerate(db.Nsa[starting_board])
             if count == max_count
            ])

        # Find the intent with the highest counts
        return probs

    counts = [x ** (1. / temp) for x in counts]
    counts_sum = float(sum(counts))
    probs = [x / counts_sum for x in counts]
    return probs
