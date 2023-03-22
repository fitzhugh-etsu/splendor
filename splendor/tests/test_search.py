import unittest

import splendor.actions as actions
import splendor.search as search

from splendor.models import Bank, Card, Game, Gems, Player
from splendor.agents.idiot import IdiotAgent

class TestSearch(unittest.TestCase):

    def test_single_search_run(self):
        game = Game.setup_game(seed=1)
        agent = IdiotAgent(seed=5)

        # Test it stays hashable
        intent = agent.evaluate(game)
        -intent

        action, intent = search.get_agent_intent(
            game,
            agent,
            simulations=100,
            seed=1)

