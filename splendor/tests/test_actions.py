import unittest

import splendor.actions as actions
import splendor.game as game


class TestActions(unittest.TestCase):
    def test_valid_actions(self):
        tabletop = game.setup_game(seed=1)
        self.assertEqual(
            [],
            list(actions.valid_actions(tabletop)))
