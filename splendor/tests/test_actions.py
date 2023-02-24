import unittest

import splendor.actions as actions
from splendor.actions import ValidPlayerActions
from splendor.types import Gems, Tabletop


class TestActions(unittest.TestCase):
    def test_valid_actions(self):
        tabletop = Tabletop.setup_game(seed=1)
        self.assertEqual(
            set((
                ValidPlayerActions.PICK_DSE,
                ValidPlayerActions.PICK_DSR,
                ValidPlayerActions.PICK_DSO,
                ValidPlayerActions.PICK_DER,
                ValidPlayerActions.PICK_DEO,
                ValidPlayerActions.PICK_DRO,
                ValidPlayerActions.PICK_SER,
                ValidPlayerActions.PICK_SEO,
                ValidPlayerActions.PICK_SRO,
                ValidPlayerActions.PICK_ERO,
                ValidPlayerActions.PICK_DD,
                ValidPlayerActions.PICK_SS,
                ValidPlayerActions.PICK_EE,
                ValidPlayerActions.PICK_RR,
                ValidPlayerActions.PICK_OO,
                ValidPlayerActions.RESERVE_TIER_0,
                ValidPlayerActions.RESERVE_TIER_0_0,
                ValidPlayerActions.RESERVE_TIER_0_1,
                ValidPlayerActions.RESERVE_TIER_0_2,
                ValidPlayerActions.RESERVE_TIER_0_3,
                ValidPlayerActions.RESERVE_TIER_1,
                ValidPlayerActions.RESERVE_TIER_1_0,
                ValidPlayerActions.RESERVE_TIER_1_1,
                ValidPlayerActions.RESERVE_TIER_1_2,
                ValidPlayerActions.RESERVE_TIER_1_3,
                ValidPlayerActions.RESERVE_TIER_2,
                ValidPlayerActions.RESERVE_TIER_2_0,
                ValidPlayerActions.RESERVE_TIER_2_1,
                ValidPlayerActions.RESERVE_TIER_2_2,
                ValidPlayerActions.RESERVE_TIER_2_3)),
            set(actions.valid_actions(tabletop)))

    def test_valid_actions_no_gem_type(self):
        tabletop = Tabletop.setup_game(seed=1)
        tabletop = tabletop._replace(
            # Update to have 0 emerald
            bank=tabletop.bank._replace(emerald=0))

        self.assertEqual(
            set((
                ValidPlayerActions.PICK_DSR,
                ValidPlayerActions.PICK_DSO,
                ValidPlayerActions.PICK_DRO,
                ValidPlayerActions.PICK_SRO,
                ValidPlayerActions.PICK_DD,
                ValidPlayerActions.PICK_SS,
                ValidPlayerActions.PICK_RR,
                ValidPlayerActions.PICK_OO,
                ValidPlayerActions.RESERVE_TIER_0,
                ValidPlayerActions.RESERVE_TIER_0_0,
                ValidPlayerActions.RESERVE_TIER_0_1,
                ValidPlayerActions.RESERVE_TIER_0_2,
                ValidPlayerActions.RESERVE_TIER_0_3,
                ValidPlayerActions.RESERVE_TIER_1,
                ValidPlayerActions.RESERVE_TIER_1_0,
                ValidPlayerActions.RESERVE_TIER_1_1,
                ValidPlayerActions.RESERVE_TIER_1_2,
                ValidPlayerActions.RESERVE_TIER_1_3,
                ValidPlayerActions.RESERVE_TIER_2,
                ValidPlayerActions.RESERVE_TIER_2_0,
                ValidPlayerActions.RESERVE_TIER_2_1,
                ValidPlayerActions.RESERVE_TIER_2_2,
                ValidPlayerActions.RESERVE_TIER_2_3)),
            set(actions.valid_actions(tabletop)))

    def test_valid_actions_one_gem_type(self):
        tabletop = Tabletop.setup_game(seed=1)
        tabletop = tabletop._replace(
            # Update to have 0 emerald
            bank=tabletop.bank._replace(emerald=1))

        self.assertEqual(
            set((
                ValidPlayerActions.PICK_DSE,
                ValidPlayerActions.PICK_DSR,
                ValidPlayerActions.PICK_DSO,
                ValidPlayerActions.PICK_DER,
                ValidPlayerActions.PICK_DEO,
                ValidPlayerActions.PICK_DRO,
                ValidPlayerActions.PICK_SER,
                ValidPlayerActions.PICK_SEO,
                ValidPlayerActions.PICK_SRO,
                ValidPlayerActions.PICK_ERO,
                ValidPlayerActions.PICK_DD,
                ValidPlayerActions.PICK_SS,
                ValidPlayerActions.PICK_RR,
                ValidPlayerActions.PICK_OO,
                ValidPlayerActions.RESERVE_TIER_0,
                ValidPlayerActions.RESERVE_TIER_0_0,
                ValidPlayerActions.RESERVE_TIER_0_1,
                ValidPlayerActions.RESERVE_TIER_0_2,
                ValidPlayerActions.RESERVE_TIER_0_3,
                ValidPlayerActions.RESERVE_TIER_1,
                ValidPlayerActions.RESERVE_TIER_1_0,
                ValidPlayerActions.RESERVE_TIER_1_1,
                ValidPlayerActions.RESERVE_TIER_1_2,
                ValidPlayerActions.RESERVE_TIER_1_3,
                ValidPlayerActions.RESERVE_TIER_2,
                ValidPlayerActions.RESERVE_TIER_2_0,
                ValidPlayerActions.RESERVE_TIER_2_1,
                ValidPlayerActions.RESERVE_TIER_2_2,
                ValidPlayerActions.RESERVE_TIER_2_3)),
            set(actions.valid_actions(tabletop)))

    def test_buy_card(self):
        pass

    def test_pick_gems(self):
        tabletop = Tabletop.setup_game(seed=1)

        self.assertTrue(
            actions.pick_gems(
                tabletop,
                Gems(diamond=2)))

        self.assertTrue(
            actions.pick_gems(
                tabletop,
                Gems(diamond=1, sapphire=1, onyx=1)))

        self.assertFalse(
            actions.pick_gems(
                tabletop,
                Gems(diamond=2, sapphire=1, onyx=2)))

        self.assertFalse(
            actions.pick_gems(
                tabletop,
                Gems(diamond=4)))

        self.assertFalse(
            actions.pick_gems(
                tabletop,
                Gems(diamond=99)))
