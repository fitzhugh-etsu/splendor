import unittest

import splendor.actions as actions
import splendor.models.actions as model_actions
from splendor.actions import (ValidGemPaybackActions, ValidNobleActions,
                              ValidPlayerActions)
from splendor.models import Bank, Card, Game, Gems, Player


class TestActions(unittest.TestCase):
    def test_valid_actions(self):
        game = Game.setup_game(seed=1)
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

                ValidPlayerActions.PICK_SO,
                ValidPlayerActions.PICK_DE,
                ValidPlayerActions.PICK_SE,
                ValidPlayerActions.PICK_DO,
                ValidPlayerActions.PICK_DR,
                ValidPlayerActions.PICK_EO,
                ValidPlayerActions.PICK_RO,
                ValidPlayerActions.PICK_ER,
                ValidPlayerActions.PICK_SR,
                ValidPlayerActions.PICK_DS,

                ValidPlayerActions.PICK_D,
                ValidPlayerActions.PICK_S,
                ValidPlayerActions.PICK_O,
                ValidPlayerActions.PICK_E,
                ValidPlayerActions.PICK_R,

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
            set([a.action for a in actions.valid_actions(game)]))

    def test_valid_actions_no_gem_type(self):
        game = Game.setup_game(seed=1)
        game = game._replace(
            # Update to have 0 emerald
            bank=game.bank._replace(emerald=0))

        self.assertEqual(
            set((
                ValidPlayerActions.PICK_DSR,
                ValidPlayerActions.PICK_DSO,
                ValidPlayerActions.PICK_DRO,
                ValidPlayerActions.PICK_SRO,

                ValidPlayerActions.PICK_SO,
                ValidPlayerActions.PICK_DO,
                ValidPlayerActions.PICK_DR,
                ValidPlayerActions.PICK_RO,
                ValidPlayerActions.PICK_SR,
                ValidPlayerActions.PICK_DS,

                ValidPlayerActions.PICK_D,
                ValidPlayerActions.PICK_S,
                ValidPlayerActions.PICK_O,
                ValidPlayerActions.PICK_R,

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
            set([a.action for a in actions.valid_actions(game)]))

    def test_valid_actions_one_gem_type(self):
        game = Game.setup_game(seed=1)
        game = game._replace(
            # Update to have 1 emerald
            bank=game.bank._replace(emerald=1))

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

                ValidPlayerActions.PICK_SO,
                ValidPlayerActions.PICK_DE,
                ValidPlayerActions.PICK_SE,
                ValidPlayerActions.PICK_DO,
                ValidPlayerActions.PICK_DR,
                ValidPlayerActions.PICK_EO,
                ValidPlayerActions.PICK_RO,
                ValidPlayerActions.PICK_ER,
                ValidPlayerActions.PICK_SR,
                ValidPlayerActions.PICK_DS,

                ValidPlayerActions.PICK_D,
                ValidPlayerActions.PICK_S,
                ValidPlayerActions.PICK_O,
                ValidPlayerActions.PICK_E,
                ValidPlayerActions.PICK_R,

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
            set([a.action for a in actions.valid_actions(game)]))

    def test_buy_card(self):
        pass

    def test_pick_gems(self):
        game = Game.setup_game(seed=1)

        self.assertTrue(
            model_actions.pick_gems(
                game,
                Gems(diamond=2)))

        self.assertTrue(
            model_actions.pick_gems(
                game,
                Gems(diamond=1, sapphire=1, onyx=1)))

        self.assertFalse(
            model_actions.pick_gems(
                game,
                Gems(diamond=2, sapphire=1, onyx=2)))

        self.assertFalse(
            model_actions.pick_gems(
                game,
                Gems(diamond=4)))

        self.assertFalse(
            model_actions.pick_gems(
                game,
                Gems(diamond=99)))

    def test_eval_action(self):
        game = Game.setup_game(seed=1, players=2)
        self.assertEqual(0, game.turn)


        # First player can pick EE, but not second
        game = actions.eval_action(game, ValidPlayerActions.PICK_SS)

        self.assertTrue(game)
        self.assertEqual(1, game.turn)
        self.assertEqual(2, game.bank.sapphire)
        self.assertEqual(Bank(sapphire=2), game.players[0].bank)
        self.assertEqual(Bank(), game.players[1].bank)

        # Not pick EE, but not second
        self.assertTrue(
            ValidPlayerActions.PICK_SS not in actions.valid_actions(game))

        game = actions.eval_action(game, ValidPlayerActions.PICK_OO)
        self.assertEqual(2, game.turn)
        self.assertEqual(2, game.bank.sapphire)
        self.assertEqual(2, game.bank.onyx)

        self.assertEqual(Bank(sapphire=2), game.players[0].bank)
        self.assertEqual(Bank(onyx=2), game.players[1].bank)

        # Reserve Card!
        self.assertTrue(
            ValidPlayerActions.BUY_RESERVED_0 not in actions.valid_actions(game))
        card_to_reserve = game.decks[0][4]

        game = actions.eval_action(game, ValidPlayerActions.RESERVE_TIER_0)

        self.assertEqual(3, game.turn)
        self.assertEqual(39, len(game.decks[0]))
        self.assertEqual((card_to_reserve._replace(hidden=True),), game.players[0].reserved)
        self.assertEqual(Bank(sapphire=2, gold=1), game.players[0].bank)
        self.assertEqual(Bank(onyx=2), game.players[1].bank)

        # Reserve Card
        self.assertTrue(
            ValidPlayerActions.BUY_RESERVED_0 not in actions.valid_actions(game))
        card_to_reserve = game.decks[0][4]
        game = actions.eval_action(game, ValidPlayerActions.RESERVE_TIER_0)
        self.assertEqual(4, game.turn)
        self.assertEqual(38, len(game.decks[0]))
        self.assertEqual((card_to_reserve._replace(hidden=True),), game.players[1].reserved)
        self.assertEqual(Bank(sapphire=2, gold=1), game.players[0].bank)
        self.assertEqual(Bank(onyx=2, gold=1), game.players[1].bank)

        # Reserve Card!
        self.assertTrue(
            ValidPlayerActions.BUY_RESERVED_0 not in actions.valid_actions(game))
        card_to_reserve = game.decks[0][4]
        game = actions.eval_action(game, ValidPlayerActions.RESERVE_TIER_0)
        self.assertEqual(5, game.turn)
        self.assertEqual(37, len(game.decks[0]))
        self.assertEqual(2, len(game.players[0].reserved))
        # It's hidden
        self.assertEqual(card_to_reserve._replace(hidden=True), game.players[0].reserved[0])
        self.assertEqual(Bank(sapphire=2, gold=2), game.players[0].bank)
        self.assertEqual(Bank(onyx=2, gold=1), game.players[1].bank)

        # Reserve Card
        self.assertTrue(
            ValidPlayerActions.BUY_RESERVED_0 not in actions.valid_actions(game))
        card_to_reserve = game.decks[0][4]
        game = actions.eval_action(game, ValidPlayerActions.RESERVE_TIER_0)
        self.assertEqual(6, game.turn)
        self.assertEqual(36, len(game.decks[0]))
        self.assertEqual(2, len(game.players[1].reserved))
        self.assertEqual(card_to_reserve._replace(hidden=True), game.players[1].reserved[0])
        self.assertEqual(Bank(sapphire=2, gold=2), game.players[0].bank)
        self.assertEqual(Bank(onyx=2, gold=2), game.players[1].bank)

        self.assertEqual(
            Bank(
                diamond=4.0,
                sapphire=2.0,
                emerald=4.0,
                ruby=4.0,
                onyx=2.0,
                gold=1),
            game.bank)

        # Player 0 turn can now buy RESERVED_0 and _1
        self.assertTrue(
            ValidPlayerActions.BUY_RESERVED_1 in [a.action for a in actions.valid_actions(game)])
        self.assertTrue(
            ValidPlayerActions.BUY_RESERVED_0 in [a.action for a in actions.valid_actions(game)])

        game = actions.eval_action(game, ValidPlayerActions.BUY_RESERVED_0)
        self.assertEqual(7, game.turn)

        # Should have returned the tkens??
        # Step through
        self.assertEqual(
            Bank(
                diamond=4.0,
                sapphire=3.0,
                emerald=4.0,
                ruby=4.0,
                onyx=2.0,
                gold=3),
            game.bank)
        self.assertEqual(36, len(game.decks[0]))
        self.assertEqual(1, len(game.players[0].reserved))
        self.assertEqual(2, len(game.players[1].reserved))
        # 2 diamond + 1 sapphire cost == 2 gold and 1 sapphire spend => 1 sapphire left
        self.assertEqual(Bank(sapphire=1), game.players[0].bank)
        self.assertEqual(Bank(onyx=2, gold=2), game.players[1].bank)

        # Player 1 turn can now buy RESERVED_0 and _1
        self.assertTrue(
            ValidPlayerActions.BUY_RESERVED_1 in [a.action for a in actions.valid_actions(game)])
        game = actions.eval_action(game, ValidPlayerActions.BUY_RESERVED_1)
        self.assertEqual(8, game.turn)
        self.assertEqual(36, len(game.decks[0]))
        self.assertEqual(1, len(game.players[0].reserved))
        self.assertEqual(1, len(game.players[1].reserved))
        self.assertTrue(game.players[1].reserved[0])
        self.assertEqual(Bank(sapphire=1), game.players[0].bank)

        # 4 onyx cost => 2 onyx + 2 gold spent => 0 bank
        self.assertEqual(Bank(), game.players[1].bank)

    def test_visiting_nobles(self):
        game = Game.setup_game(seed=1, players=2)
        self.assertEqual(0, game.turn)

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
        game = game._replace(
            turn=1,
            players=(new_player,))

        noble0 = game.nobles_deck[0]

        visiting_nobles = list(actions.valid_nobles_for_last_player(game))
        self.assertEqual(ValidNobleActions.NOBLE_0, visiting_nobles[0].action)

        game = visiting_nobles[0].game

        # don't change the turn
        self.assertEqual(1, game.turn)
        self.assertEqual(game.players[0].nobles[0], noble0)

    def test_returning_gems(self):
        game = Game.setup_game(seed=1, players=2)
        self.assertEqual(0, game.turn)
        self.assertEqual(
            tuple(),
            tuple(list(actions.valid_payback_actions_for_last_player(game))))

        self.assertEqual(
            (ValidGemPaybackActions.RETURN_E,),
            tuple([a.action for a in actions.valid_payback_actions_for_last_player(
                game._replace(
                    players=(Player(
                        bank=Bank(
                            emerald=11, )),)))]))

        self.assertEqual(
            (ValidGemPaybackActions.RETURN_D,),
            tuple([a.action for a in (actions.valid_payback_actions_for_last_player(
                game._replace(
                    players=(Player(
                        bank=Bank(
                            diamond=11)),))))]))

        self.assertEqual(
            (ValidGemPaybackActions.RETURN_S,),
            tuple([a.action for a in actions.valid_payback_actions_for_last_player(
                game._replace(
                    players=(Player(
                        bank=Bank(
                            sapphire=11)),)))]))

        self.assertEqual(
            (ValidGemPaybackActions.RETURN_R,),
            tuple([a.action for a in actions.valid_payback_actions_for_last_player(
                game._replace(
                    players=(Player(
                        bank=Bank(
                            ruby=11)),)))]))

        self.assertEqual(
            (ValidGemPaybackActions.RETURN_O,),
            tuple([a.action for a in actions.valid_payback_actions_for_last_player(
                game._replace(
                    players=(Player(
                        bank=Bank(
                            onyx=11)),)))]))

        self.assertEqual(
            (ValidGemPaybackActions.RETURN_G,),
            tuple([a.action for a in actions.valid_payback_actions_for_last_player(
                game._replace(
                    players=(Player(
                        bank=Bank(
                            gold=11)),)))]))
