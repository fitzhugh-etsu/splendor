import unittest

import splendor.actions as actions
from splendor.actions import ValidPlayerActions
from splendor.types import Bank, Card, Gems, Player, Tabletop


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

    def test_apply_action(self):
        tabletop = Tabletop.setup_game(seed=1, players=2)
        self.assertEqual(0, tabletop.turn)

        # First player can pick EE, but not second
        tabletop = actions.apply_action(tabletop, ValidPlayerActions.PICK_SS)
        self.assertTrue(tabletop)
        self.assertEqual(1, tabletop.turn)
        self.assertEqual(2, tabletop.bank.sapphire)
        self.assertEqual(Bank(sapphire=2), tabletop.players[0].bank)
        self.assertEqual(Bank(), tabletop.players[1].bank)

        # Not pick EE, but not second
        self.assertTrue(
            ValidPlayerActions.PICK_SS not in actions.valid_actions(tabletop))

        tabletop = actions.apply_action(tabletop, ValidPlayerActions.PICK_OO)
        self.assertEqual(2, tabletop.turn)
        self.assertEqual(2, tabletop.bank.sapphire)
        self.assertEqual(2, tabletop.bank.onyx)

        self.assertEqual(Bank(sapphire=2), tabletop.players[0].bank)
        self.assertEqual(Bank(onyx=2), tabletop.players[1].bank)

        # Reserve Card!
        self.assertTrue(
            ValidPlayerActions.BUY_RESERVED_0 not in actions.valid_actions(tabletop))
        card_to_reserve = tabletop.decks[0][4]
        tabletop = actions.apply_action(tabletop, ValidPlayerActions.RESERVE_TIER_0)
        self.assertEqual(3, tabletop.turn)
        self.assertEqual(39, len(tabletop.decks[0]))
        self.assertEqual((card_to_reserve,), tabletop.players[0].reserved)
        self.assertEqual(Bank(sapphire=2, gold=1), tabletop.players[0].bank)
        self.assertEqual(Bank(onyx=2), tabletop.players[1].bank)

        # Reserve Card
        self.assertTrue(
            ValidPlayerActions.BUY_RESERVED_0 not in actions.valid_actions(tabletop))
        card_to_reserve = tabletop.decks[0][4]
        tabletop = actions.apply_action(tabletop, ValidPlayerActions.RESERVE_TIER_0)
        self.assertEqual(4, tabletop.turn)
        self.assertEqual(38, len(tabletop.decks[0]))
        self.assertEqual((card_to_reserve,), tabletop.players[1].reserved)
        self.assertEqual(Bank(sapphire=2, gold=1), tabletop.players[0].bank)
        self.assertEqual(Bank(onyx=2, gold=1), tabletop.players[1].bank)

        # Reserve Card!
        self.assertTrue(
            ValidPlayerActions.BUY_RESERVED_0 not in actions.valid_actions(tabletop))
        card_to_reserve = tabletop.decks[0][4]
        tabletop = actions.apply_action(tabletop, ValidPlayerActions.RESERVE_TIER_0)
        self.assertEqual(5, tabletop.turn)
        self.assertEqual(37, len(tabletop.decks[0]))
        self.assertEqual(2, len(tabletop.players[0].reserved))
        self.assertEqual(card_to_reserve, tabletop.players[0].reserved[0])
        self.assertEqual(Bank(sapphire=2, gold=2), tabletop.players[0].bank)
        self.assertEqual(Bank(onyx=2, gold=1), tabletop.players[1].bank)

        # Reserve Card
        self.assertTrue(
            ValidPlayerActions.BUY_RESERVED_0 not in actions.valid_actions(tabletop))
        card_to_reserve = tabletop.decks[0][4]
        tabletop = actions.apply_action(tabletop, ValidPlayerActions.RESERVE_TIER_0)
        self.assertEqual(6, tabletop.turn)
        self.assertEqual(36, len(tabletop.decks[0]))
        self.assertEqual(2, len(tabletop.players[1].reserved))
        self.assertEqual(card_to_reserve, tabletop.players[1].reserved[0])
        self.assertEqual(Bank(sapphire=2, gold=2), tabletop.players[0].bank)
        self.assertEqual(Bank(onyx=2, gold=2), tabletop.players[1].bank)

        # Player 0 turn can now buy RESERVED_0 and _1
        self.assertTrue(
            ValidPlayerActions.BUY_RESERVED_1 in actions.valid_actions(tabletop))
        self.assertTrue(
            ValidPlayerActions.BUY_RESERVED_0 in actions.valid_actions(tabletop))

        tabletop = actions.apply_action(tabletop, ValidPlayerActions.BUY_RESERVED_0)
        self.assertEqual(7, tabletop.turn)
        self.assertEqual(36, len(tabletop.decks[0]))
        self.assertEqual(1, len(tabletop.players[0].reserved))
        self.assertEqual(2, len(tabletop.players[1].reserved))
        # 2 diamond + 1 sapphire cost == 2 gold and 1 sapphire spend => 1 sapphire left
        self.assertEqual(Bank(sapphire=1), tabletop.players[0].bank)
        self.assertEqual(Bank(onyx=2, gold=2), tabletop.players[1].bank)

        # Player 1 turn can now buy RESERVED_0 and _1
        self.assertTrue(
            ValidPlayerActions.BUY_RESERVED_1 in actions.valid_actions(tabletop))
        tabletop = actions.apply_action(tabletop, ValidPlayerActions.BUY_RESERVED_1)
        self.assertEqual(8, tabletop.turn)
        self.assertEqual(36, len(tabletop.decks[0]))
        self.assertEqual(1, len(tabletop.players[0].reserved))
        self.assertEqual(1, len(tabletop.players[1].reserved))
        self.assertTrue(tabletop.players[1].reserved[0])
        self.assertEqual(Bank(sapphire=1), tabletop.players[0].bank)

        # 4 onyx cost => 2 onyx + 2 gold spent => 0 bank
        self.assertEqual(Bank(), tabletop.players[1].bank)

    def test_visiting_nobles(self):
        tabletop = Tabletop.setup_game(seed=1, players=2)
        self.assertEqual(0, tabletop.turn)

        # Cheat, noble needs 4S 4E
        new_player = Player(
            purchased=(
                Card(bonus=Gems(sapphire=1)),
                Card(bonus=Gems(sapphire=1)),
                Card(bonus=Gems(sapphire=1)),
                Card(bonus=Gems(sapphire=1)),
                Card(bonus=Gems(emerald=1)),
                Card(bonus=Gems(emerald=1)),
                Card(bonus=Gems(emerald=1)),
                Card(bonus=Gems(emerald=1))))

        # Turn "finished", now we can check
        tabletop = tabletop._replace(
            turn=1,
            players=(new_player,))

        visiting_nobles = actions.visiting_nobles_for_last_player(tabletop)
        self.assertEqual(((0, tabletop.nobles_deck[0]),), visiting_nobles)

        tabletop = actions.accept_noble(tabletop, 0)

        # don't change the turn
        self.assertEqual(1, tabletop.turn)
        self.assertEqual(tuple([n[1] for n in visiting_nobles]), tabletop.players[0].nobles)
