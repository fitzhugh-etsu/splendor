import unittest

from splendor.models import Bank, Card, Game, Gems


class TestModels(unittest.TestCase):
    def test_gold_actions(self):
        self.assertTrue(
            Bank.is_solvent(
                Bank.pickup_gold(
                    Bank(gold=10),
                    gold=1)))

        self.assertFalse(
            Bank.is_solvent(
                Bank.pickup_gold(
                    Bank(gold=0),
                    gold=1)))

    def test_remove_card_from_deck(self):
        decks = (
            (Card(points=1), Card(points=2), Card(points=3)),
            (Card(points=11), Card(points=12), Card(points=13)),
            (Card(points=21), Card(points=22), Card(points=23)))

        game = Game.setup_game(seed=0)._replace(decks=decks)

        self.assertEqual((
            (Card(points=2), Card(points=3)),
            (Card(points=11), Card(points=12), Card(points=13)),
            (Card(points=21), Card(points=22), Card(points=23))),
            Game.remove_card_from_deck(game, 0, 0).decks)

        self.assertEqual((
            (Card(points=1), Card(points=2), Card(points=3)),
            (Card(points=11), Card(points=13)),
            (Card(points=21), Card(points=22), Card(points=23))),
            Game.remove_card_from_deck(game, 1, 1).decks)

        self.assertEqual((
            (Card(points=1), Card(points=2), Card(points=3)),
            (Card(points=11), Card(points=12), Card(points=13)),
            (Card(points=21), Card(points=22))),
            Game.remove_card_from_deck(game, 2, 2).decks)

    def test_player_purchase_card(self):
        pass

    def test_can_afford(self):
        self.assertTrue(
            Bank.is_solvent(
                Bank.pay_gems(
                    Bank(gold=4),
                    None,
                    Gems(diamond=3))))

        self.assertFalse(
            Bank.is_solvent(
                Bank.pay_gems(
                    Bank(gold=3),
                    None,
                    Gems(diamond=4))))

        self.assertEqual(
            Bank(diamond=1, sapphire=-2),
            Bank.pay_gems(
                Bank(diamond=4, sapphire=6, gold=0),
                None,
                Gems(diamond=3, sapphire=8),
                allow_gold=False))

        self.assertEqual(
            Bank(diamond=1, sapphire=0, gold=-2),
            Bank.pay_gems(
                Bank(diamond=4, sapphire=6, gold=0),
                None,
                Gems(diamond=3, sapphire=8),
                allow_gold=True))

        self.assertEqual(
            Bank(diamond=1),
            Bank.pay_gems(
                Bank(diamond=4),
                None,
                Gems(diamond=3),
                allow_gold=False))

        self.assertEqual(
            Bank(diamond=1),
            Bank.pay_gems(
                Bank(diamond=4, sapphire=3),
                # Bonus
                Gems(sapphire=5),
                Gems(diamond=3, sapphire=8)))

        self.assertEqual(
            Bank(diamond=1, gold=0),
            Bank.pay_gems(
                Bank(diamond=4, gold=5),
                # Bonus
                Gems(sapphire=5, onyx=3, ruby=7),
                # Cost
                Gems(diamond=3, emerald=5)))
