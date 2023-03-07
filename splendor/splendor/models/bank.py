from typing import NamedTuple

from .gems import Gems


class Bank(NamedTuple):
    diamond: int = 0
    sapphire: int = 0
    emerald: int = 0
    ruby: int = 0
    onyx: int = 0
    gold: int = 0

    @staticmethod
    def difference(b1, b2):
        return Bank(*[b1[i] - b2[i] for i in range(len(Bank()))])

    @staticmethod
    def is_solvent(bank):
        return all([v >= 0 for v in bank])

    @staticmethod
    def pickup_gold(bank, gold=1):
        return bank._replace(gold=bank.gold - gold)

    @staticmethod
    def add_gold(bank, gold=1):
        return bank._replace(gold=bank.gold + gold)

    @staticmethod
    def pay_gems(bank, bonus, gems, allow_gold=True):
        new_bank = Bank.subtract_gems(
            bank,
            # Discount from bonus (cost of a card after bonus can't go negative, so max to 0)
            Gems.subtract(
                gems,
                bonus or Gems(),
                allow_negative=False),
            allow_negative=True)

        if allow_gold:
            return Bank(
                # Assuming all debts are covered, we max(0,...)  the error will play out in gold < > 0
                # Order of Bank and Gems is ==
                *[max(0, new_bank[i]) for i in range(len(Gems()))],
                # Gold remaining is previous + any deficit spending we did.
                gold=new_bank.gold + sum([new_bank[i] for i in range(len(Gems())) if new_bank[i] < 0]))

        else:
            return new_bank

    @staticmethod
    def receive_bank(b1, b2, **kwargs):
        # This is ok b/c of order of things (and FAST)
        return Bank(*Gems.add(b1, b2), gold=b1.gold + b2.gold)

    @staticmethod
    def add_gems(bank, g1, **kwargs):
        # This is ok b/c of order of things (and FAST)
        return Bank(*Gems.add(bank, g1, **kwargs), gold=bank.gold)

    @staticmethod
    def subtract_gems(bank, g1, **kwargs):
        # This is ok b/c of order of things (and FAST)
        return Bank(*Gems.subtract(bank, g1, **kwargs), gold=bank.gold)

