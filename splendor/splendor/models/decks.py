import random

from .card import Card
from .gems import Gems
from .noble import Noble

EMERALD = Gems(emerald=1.0)
SAPPHIRE = Gems(sapphire=1.0)
RUBY = Gems(ruby=1.0)
DIAMOND = Gems(diamond=1.0)
ONYX = Gems(onyx=1.0)

def tier_0_deck(seed=None):
    all_cards = (
        Card(points=0, bonus=ONYX, cost=Gems(diamond=1, sapphire=1, emerald=1, ruby=1, onyx=0)),
        Card(points=0, bonus=ONYX, cost=Gems(diamond=1, sapphire=2, emerald=1, ruby=1, onyx=0)),
        Card(points=0, bonus=ONYX, cost=Gems(diamond=2, sapphire=2, emerald=0, ruby=1, onyx=0)),
        Card(points=0, bonus=ONYX, cost=Gems(diamond=0, sapphire=0, emerald=1, ruby=3, onyx=1)),
        Card(points=0, bonus=ONYX, cost=Gems(diamond=0, sapphire=0, emerald=2, ruby=1, onyx=0)),
        Card(points=0, bonus=ONYX, cost=Gems(diamond=2, sapphire=0, emerald=2, ruby=0, onyx=0)),
        Card(points=0, bonus=ONYX, cost=Gems(diamond=0, sapphire=0, emerald=3, ruby=0, onyx=0)),
        Card(points=1, bonus=ONYX, cost=Gems(diamond=0, sapphire=4, emerald=0, ruby=0, onyx=0)),

        Card(points=0, bonus=SAPPHIRE, cost=Gems(diamond=1, sapphire=0, emerald=1, ruby=1, onyx=1)),
        Card(points=0, bonus=SAPPHIRE, cost=Gems(diamond=1, sapphire=0, emerald=1, ruby=2, onyx=1)),
        Card(points=0, bonus=SAPPHIRE, cost=Gems(diamond=1, sapphire=0, emerald=2, ruby=2, onyx=0)),
        Card(points=0, bonus=SAPPHIRE, cost=Gems(diamond=0, sapphire=1, emerald=3, ruby=1, onyx=0)),
        Card(points=0, bonus=SAPPHIRE, cost=Gems(diamond=1, sapphire=0, emerald=0, ruby=0, onyx=2)),
        Card(points=0, bonus=SAPPHIRE, cost=Gems(diamond=0, sapphire=0, emerald=2, ruby=0, onyx=2)),
        Card(points=0, bonus=SAPPHIRE, cost=Gems(diamond=0, sapphire=0, emerald=0, ruby=0, onyx=3)),
        Card(points=1, bonus=SAPPHIRE, cost=Gems(diamond=0, sapphire=0, emerald=0, ruby=4, onyx=0)),

        Card(points=0, bonus=DIAMOND, cost=Gems(diamond=0, sapphire=1, emerald=1, ruby=1, onyx=1)),
        Card(points=0, bonus=DIAMOND, cost=Gems(diamond=0, sapphire=1, emerald=2, ruby=1, onyx=1)),
        Card(points=0, bonus=DIAMOND, cost=Gems(diamond=0, sapphire=2, emerald=2, ruby=0, onyx=1)),
        Card(points=0, bonus=DIAMOND, cost=Gems(diamond=3, sapphire=1, emerald=0, ruby=0, onyx=1)),
        Card(points=0, bonus=DIAMOND, cost=Gems(diamond=0, sapphire=0, emerald=0, ruby=2, onyx=1)),
        Card(points=0, bonus=DIAMOND, cost=Gems(diamond=0, sapphire=2, emerald=0, ruby=0, onyx=2)),
        Card(points=0, bonus=DIAMOND, cost=Gems(diamond=0, sapphire=3, emerald=0, ruby=0, onyx=0)),
        Card(points=1, bonus=DIAMOND, cost=Gems(diamond=0, sapphire=0, emerald=4, ruby=0, onyx=0)),

        Card(points=0, bonus=EMERALD, cost=Gems(diamond=1, sapphire=1, emerald=0, ruby=1, onyx=1)),
        Card(points=0, bonus=EMERALD, cost=Gems(diamond=1, sapphire=1, emerald=0, ruby=1, onyx=2)),
        Card(points=0, bonus=EMERALD, cost=Gems(diamond=0, sapphire=1, emerald=0, ruby=2, onyx=2)),
        Card(points=0, bonus=EMERALD, cost=Gems(diamond=1, sapphire=3, emerald=1, ruby=0, onyx=0)),
        Card(points=0, bonus=EMERALD, cost=Gems(diamond=2, sapphire=1, emerald=0, ruby=0, onyx=0)),
        Card(points=0, bonus=EMERALD, cost=Gems(diamond=0, sapphire=2, emerald=0, ruby=2, onyx=0)),
        Card(points=0, bonus=EMERALD, cost=Gems(diamond=0, sapphire=0, emerald=0, ruby=3, onyx=0)),
        Card(points=1, bonus=EMERALD, cost=Gems(diamond=0, sapphire=0, emerald=0, ruby=0, onyx=4)),

        Card(points=0, bonus=RUBY, cost=Gems(diamond=1, sapphire=1, emerald=1, ruby=0, onyx=1)),
        Card(points=0, bonus=RUBY, cost=Gems(diamond=2, sapphire=1, emerald=1, ruby=0, onyx=1)),
        Card(points=0, bonus=RUBY, cost=Gems(diamond=2, sapphire=0, emerald=1, ruby=0, onyx=2)),
        Card(points=0, bonus=RUBY, cost=Gems(diamond=1, sapphire=0, emerald=0, ruby=1, onyx=3)),
        Card(points=0, bonus=RUBY, cost=Gems(diamond=0, sapphire=2, emerald=1, ruby=0, onyx=0)),
        Card(points=0, bonus=RUBY, cost=Gems(diamond=2, sapphire=0, emerald=0, ruby=2, onyx=0)),
        Card(points=0, bonus=RUBY, cost=Gems(diamond=3, sapphire=0, emerald=0, ruby=0, onyx=0)),
        Card(points=1, bonus=RUBY, cost=Gems(diamond=4, sapphire=0, emerald=0, ruby=0, onyx=0)))

    return tuple(random.Random(seed).sample(all_cards, len(all_cards)))

def tier_1_deck(seed=None):
    all_cards = (
        Card(points=1, bonus=ONYX, cost=Gems(diamond=3, sapphire=2, emerald=2, ruby=0, onyx=0)),
        Card(points=1, bonus=ONYX, cost=Gems(diamond=3, sapphire=0, emerald=3, ruby=0, onyx=2)),
        Card(points=2, bonus=ONYX, cost=Gems(diamond=0, sapphire=1, emerald=4, ruby=2, onyx=0)),
        Card(points=2, bonus=ONYX, cost=Gems(diamond=0, sapphire=0, emerald=5, ruby=3, onyx=0)),
        Card(points=2, bonus=ONYX, cost=Gems(diamond=5, sapphire=0, emerald=0, ruby=0, onyx=0)),
        Card(points=3, bonus=ONYX, cost=Gems(diamond=0, sapphire=0, emerald=0, ruby=0, onyx=6)),

        Card(points=1, bonus=SAPPHIRE, cost=Gems(diamond=0, sapphire=2, emerald=2, ruby=3, onyx=0)),
        Card(points=1, bonus=SAPPHIRE, cost=Gems(diamond=0, sapphire=2, emerald=3, ruby=0, onyx=3)),
        Card(points=2, bonus=SAPPHIRE, cost=Gems(diamond=5, sapphire=3, emerald=0, ruby=0, onyx=0)),
        Card(points=2, bonus=SAPPHIRE, cost=Gems(diamond=2, sapphire=0, emerald=0, ruby=1, onyx=4)),
        Card(points=2, bonus=SAPPHIRE, cost=Gems(diamond=0, sapphire=5, emerald=0, ruby=0, onyx=0)),
        Card(points=3, bonus=SAPPHIRE, cost=Gems(diamond=0, sapphire=6, emerald=0, ruby=0, onyx=0)),

        Card(points=1, bonus=DIAMOND, cost=Gems(diamond=0, sapphire=0, emerald=3, ruby=2, onyx=2)),
        Card(points=1, bonus=DIAMOND, cost=Gems(diamond=2, sapphire=3, emerald=0, ruby=3, onyx=0)),
        Card(points=2, bonus=DIAMOND, cost=Gems(diamond=0, sapphire=0, emerald=1, ruby=4, onyx=2)),
        Card(points=2, bonus=DIAMOND, cost=Gems(diamond=0, sapphire=0, emerald=0, ruby=5, onyx=3)),
        Card(points=2, bonus=DIAMOND, cost=Gems(diamond=0, sapphire=0, emerald=0, ruby=5, onyx=0)),
        Card(points=3, bonus=DIAMOND, cost=Gems(diamond=6, sapphire=0, emerald=0, ruby=0, onyx=0)),

        Card(points=1, bonus=EMERALD, cost=Gems(diamond=2, sapphire=3, emerald=0, ruby=0, onyx=2)),
        Card(points=1, bonus=EMERALD, cost=Gems(diamond=3, sapphire=0, emerald=2, ruby=3, onyx=0)),
        Card(points=2, bonus=EMERALD, cost=Gems(diamond=4, sapphire=2, emerald=0, ruby=0, onyx=1)),
        Card(points=2, bonus=EMERALD, cost=Gems(diamond=0, sapphire=5, emerald=3, ruby=0, onyx=0)),
        Card(points=2, bonus=EMERALD, cost=Gems(diamond=0, sapphire=0, emerald=5, ruby=0, onyx=0)),
        Card(points=3, bonus=EMERALD, cost=Gems(diamond=0, sapphire=0, emerald=6, ruby=0, onyx=0)),

        Card(points=1, bonus=RUBY, cost=Gems(diamond=2, sapphire=0, emerald=0, ruby=2, onyx=3)),
        Card(points=1, bonus=RUBY, cost=Gems(diamond=0, sapphire=3, emerald=0, ruby=2, onyx=3)),
        Card(points=2, bonus=RUBY, cost=Gems(diamond=1, sapphire=4, emerald=2, ruby=0, onyx=0)),
        Card(points=2, bonus=RUBY, cost=Gems(diamond=3, sapphire=0, emerald=0, ruby=0, onyx=5)),
        Card(points=2, bonus=RUBY, cost=Gems(diamond=0, sapphire=0, emerald=0, ruby=0, onyx=5)),
        Card(points=3, bonus=RUBY, cost=Gems(diamond=0, sapphire=0, emerald=0, ruby=6, onyx=0)))
    return tuple(random.Random(seed).sample(all_cards, len(all_cards)))

def tier_2_deck(seed=None):
    all_cards = (
        Card(points=3, bonus=ONYX, cost=Gems(diamond=3, sapphire=3, emerald=5, ruby=3, onyx=0)),
        Card(points=4, bonus=ONYX, cost=Gems(diamond=0, sapphire=0, emerald=0, ruby=7, onyx=0)),
        Card(points=4, bonus=ONYX, cost=Gems(diamond=0, sapphire=0, emerald=3, ruby=6, onyx=3)),
        Card(points=5, bonus=ONYX, cost=Gems(diamond=0, sapphire=0, emerald=0, ruby=7, onyx=3)),
        Card(points=3, bonus=SAPPHIRE, cost=Gems(diamond=3, sapphire=0, emerald=3, ruby=3, onyx=5)),
        Card(points=4, bonus=SAPPHIRE, cost=Gems(diamond=7, sapphire=0, emerald=0, ruby=0, onyx=0)),
        Card(points=4, bonus=SAPPHIRE, cost=Gems(diamond=6, sapphire=3, emerald=0, ruby=0, onyx=3)),
        Card(points=5, bonus=SAPPHIRE, cost=Gems(diamond=7, sapphire=3, emerald=0, ruby=0, onyx=0)),
        Card(points=3, bonus=DIAMOND, cost=Gems(diamond=0, sapphire=3, emerald=3, ruby=5, onyx=3)),
        Card(points=4, bonus=DIAMOND, cost=Gems(diamond=0, sapphire=0, emerald=0, ruby=0, onyx=7)),
        Card(points=4, bonus=DIAMOND, cost=Gems(diamond=3, sapphire=0, emerald=0, ruby=3, onyx=6)),
        Card(points=5, bonus=DIAMOND, cost=Gems(diamond=3, sapphire=0, emerald=0, ruby=0, onyx=7)),
        Card(points=3, bonus=EMERALD, cost=Gems(diamond=5, sapphire=3, emerald=0, ruby=3, onyx=3)),
        Card(points=4, bonus=EMERALD, cost=Gems(diamond=0, sapphire=7, emerald=0, ruby=0, onyx=0)),
        Card(points=4, bonus=EMERALD, cost=Gems(diamond=3, sapphire=6, emerald=3, ruby=0, onyx=0)),
        Card(points=5, bonus=EMERALD, cost=Gems(diamond=0, sapphire=7, emerald=3, ruby=0, onyx=0)),
        Card(points=4, bonus=RUBY, cost=Gems(diamond=0, sapphire=0, emerald=7, ruby=0, onyx=0)),
        Card(points=3, bonus=RUBY, cost=Gems(diamond=3, sapphire=5, emerald=3, ruby=0, onyx=3)),
        Card(points=4, bonus=RUBY, cost=Gems(diamond=0, sapphire=3, emerald=6, ruby=3, onyx=0)),
        Card(points=5, bonus=RUBY, cost=Gems(diamond=0, sapphire=0, emerald=7, ruby=3, onyx=0)))

    return tuple(random.Random(seed).sample(all_cards, len(all_cards)))

def nobles_deck(seed=None):
    all_cards = (
        Noble(points=3, cost=Gems(diamond=0, sapphire=0, emerald=0, ruby=4, onyx=4)),
        Noble(points=3, cost=Gems(diamond=0, sapphire=0, emerald=3, ruby=3, onyx=3)),
        Noble(points=3, cost=Gems(diamond=0, sapphire=4, emerald=4, ruby=0, onyx=0)),
        Noble(points=3, cost=Gems(diamond=4, sapphire=4, emerald=0, ruby=0, onyx=0)),
        Noble(points=3, cost=Gems(diamond=3, sapphire=3, emerald=0, ruby=0, onyx=3)),
        Noble(points=3, cost=Gems(diamond=0, sapphire=0, emerald=4, ruby=4, onyx=0)),
        Noble(points=3, cost=Gems(diamond=0, sapphire=3, emerald=3, ruby=3, onyx=0)),
        Noble(points=3, cost=Gems(diamond=4, sapphire=0, emerald=0, ruby=0, onyx=4)),
        Noble(points=3, cost=Gems(diamond=3, sapphire=3, emerald=3, ruby=0, onyx=0)),
        Noble(points=3, cost=Gems(diamond=3, sapphire=0, emerald=0, ruby=3, onyx=3)))

    return tuple(random.Random(seed).sample(all_cards, len(all_cards)))
