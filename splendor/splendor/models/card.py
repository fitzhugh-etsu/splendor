from typing import NamedTuple

from .gems import Gems


class Card(NamedTuple):
    cost: Gems = Gems()
    points: int = 0
    bonus: Gems = Gems()
    hidden: bool = False

    @staticmethod
    def to_inputs(card, hidden=False):
        if hidden:
            return Card.to_inputs(Card())
        else:
            return Gems.to_inputs(card.cost) + (card.points,) + Gems.to_inputs(card.bonus)
