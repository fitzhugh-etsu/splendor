import unittest

import splendor.actions as actions
from splendor.types import Gems, Tabletop


class TestActions(unittest.TestCase):
    def test_valid_actions(self):
        tabletop = Tabletop.setup_game(seed=1)
        self.assertEqual(
            [],
            list(actions.valid_actions(tabletop)))

    def test_buy_card(self):
        pass

    def test_pick_gems(self):
        tabletop = Tabletop.setup_game(seed=1)

        self.assertTrue(
            actions.pick_gems(
                tabletop,
                Gems(diamond=4)))

        self.assertTrue(
            actions.pick_gems(
                tabletop,
                Gems(diamond=4)))
