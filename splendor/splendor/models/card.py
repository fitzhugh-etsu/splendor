from typing import NamedTuple

from .gems import Gems


class Card(NamedTuple):
    cost: Gems = Gems()
    points: int = 0
    bonus: Gems = Gems()
    hidden: bool = False
