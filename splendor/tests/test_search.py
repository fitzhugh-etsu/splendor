import unittest

import splendor.actions as actions
import splendor.search as search

from splendor.models import Bank, Card, Game, Gems, Player
from splendor.agents import idiot

class TestSearch(unittest.TestCase):

    def test_valid_actions(self):
        game = Game.setup_game(seed=1)
        agent = idiot.create(seed=5)

        import pudb; pudb.set_trace()
        intent = search.get_agent_intent(
            game,
            agent,
            simulations=10,
            seed=1)
