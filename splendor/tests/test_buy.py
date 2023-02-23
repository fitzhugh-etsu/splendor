import unittest

import splendor.buy as buy
import splendor.data as d


class TestBuy(unittest.TestCase):
    def _equal_with_mods(self, player, card, new_bank):
        res = buy.can_afford(player, card)
        self.assertTrue(res)
        self.assertEqual(res.bank, new_bank)

    def test_can_afford(self):
        self.assertTrue(
            buy.can_afford(
                d.Player(bank=d.Bank(gold=4)),
                d.Card(cost=d.Gems(diamond=3))))

        self.assertFalse(
            buy.can_afford(
                d.Player(bank=d.Bank(gold=3)),
                d.Card(cost=d.Gems(diamond=4))))

        self.assertEqual(
            None,
            buy.can_afford(
                d.Player(
                    bank=d.Bank(diamond=4, sapphire=6)),
                d.Card(cost=d.Gems(sapphire=8, diamond=3))))

        self._equal_with_mods(
            d.Player(bank=d.Bank(diamond=4)),
            d.Card(cost=d.Gems(diamond=3)),
            d.Bank(diamond=1))

        self._equal_with_mods(
            d.Player(bank=d.Bank(diamond=4, sapphire=8)),
            d.Card(cost=d.Gems(sapphire=8, diamond=3)),
            d.Bank(diamond=1))

        self._equal_with_mods(
            d.Player(
                purchased=(
                    d.Card(bonus=d.Gems(sapphire=1)),
                    d.Card(bonus=d.Gems(sapphire=1, diamond=1))),
                bank=d.Bank(diamond=4, sapphire=6)),
            d.Card(cost=d.Gems(sapphire=8, diamond=3)),
            d.Bank(diamond=2))

        self._equal_with_mods(
            d.Player(
                purchased=(
                    d.Card(bonus=d.Gems(sapphire=1)),
                    d.Card(bonus=d.Gems(emerald=1)),
                    d.Card(bonus=d.Gems(sapphire=1, diamond=1))),
                bank=d.Bank(diamond=4, emerald=8, sapphire=6)),
            d.Card(cost=d.Gems(sapphire=8, diamond=3)),
            d.Bank(diamond=2, emerald=8))
