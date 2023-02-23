from typing import NamedTuple


class Gems(NamedTuple):
    diamond: float = 0.0
    sapphire: float = 0.0
    emerald: float = 0.0
    ruby: float = 0.0
    onyx: float = 0.0

EMERALD = Gems(emerald=1.0)
SAPPHIRE = Gems(sapphire=1.0)
RUBY = Gems(ruby=1.0)
DIAMOND = Gems(diamond=1.0)
ONYX = Gems(onyx=1.0)

class Card(NamedTuple):
    cost: Gems = Gems()
    tier: int = 0
    points: float = 0
    bonus: Gems = Gems()

class Noble(NamedTuple):
    points: float
    cost: Gems

class Bank(NamedTuple):
    diamond: int = 0
    sapphire: int = 0
    emerald: int = 0
    ruby: int = 0
    onyx: int = 0
    gold: int = 0

class Player(NamedTuple):
    reserved: tuple = ()
    nobles: tuple = ()
    purchased: tuple = ()

    # How many gems do you have
    bank: Bank = Bank()

class Tabletop(NamedTuple):
    noble_deck: tuple
    tier_0_deck: tuple
    tier_1_deck: tuple
    tier_2_deck: tuple

    bank: Bank
    players: tuple
    turn: int = 0
