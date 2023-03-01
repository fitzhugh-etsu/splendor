import random
from typing import NamedTuple

from . import defs as d


class Gems(NamedTuple):
    diamond: float = 0.0
    sapphire: float = 0.0
    emerald: float = 0.0
    ruby: float = 0.0
    onyx: float = 0.0

    @staticmethod
    def subtract(g1, g2, allow_negative=True):
        if allow_negative:
            return Gems(*[g1[i] - g2[i] for i in range(len(Gems()))])
        else:
            return Gems(*[max(0, g1[i] - g2[i]) for i in range(len(Gems()))])

    @staticmethod
    def add(g1, g2, allow_negative=True):
        return Gems(*[g1[i] + g2[i] for i in range(len(Gems()))])

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

EMERALD = Gems(emerald=1.0)
SAPPHIRE = Gems(sapphire=1.0)
RUBY = Gems(ruby=1.0)
DIAMOND = Gems(diamond=1.0)
ONYX = Gems(onyx=1.0)

class Card(NamedTuple):
    cost: Gems = Gems()
    points: float = 0
    bonus: Gems = Gems()
    hidden: bool = False

class Noble(NamedTuple):
    points: float
    cost: Gems

    @staticmethod
    def number_visible(players):
        player_count = len(players)
        if player_count >= 4:
            return 5
        elif player_count == 3:
            return 4
        else:
            return 3

    @staticmethod
    def would_visit(noble, player):
        # Gives the "BONUS" scores for all purchased cards
        player_bonus = Player.get_bonus(player)

        # Would this noble visit this player?
        # BONUS from the card (which is it?)
        if all([noble.cost[i] <= player_bonus[i] for i in range(len(Gems()))]):
            return True

class Player(NamedTuple):

    reserved: tuple = ()
    nobles: tuple = ()
    purchased: tuple = ()

    # How many gems do you have
    bank: Bank = Bank()

    @staticmethod
    def won(player):
        return Player.points(player) >= d.POINTS_FOR_WIN

    @staticmethod
    def is_turn(tabletop, player_i):
        return (tabletop.turn % len(tabletop.players)) == player_i

    @staticmethod
    def points(player):
        return sum([n.points for n in player.nobles]) + \
            sum([c.points for c in player.purchased])

    @staticmethod
    def update_bank(player, bank):
        return player._replace(bank=bank)

    @staticmethod
    def get_bonus(player):
        return Gems(*[sum([card.bonus[i] for card in player.purchased]) for i in range(len(Gems()))])

    @staticmethod
    def add_noble(player, noble):
        return player._replace(
            nobles=((noble,) + player.nobles))

    @staticmethod
    def add_card_to_purchased(player, card):
        # Make sure it isn't hidden anymore!
        return player._replace(
            purchased=((card._replace(hidden=False),) + player.purchased))

    @staticmethod
    def add_card_to_reserved(player, card):
        return player._replace(
            reserved=((card._replace(hidden=True),) + player.reserved))

    @staticmethod
    def can_reserve_card(player):
        return len(player.reserved) < d.MAX_PLAYER_RESERVATIONS

    @staticmethod
    def get_reserved(player, reserved_i):
        try:
            return player.reserved[reserved_i]
        except IndexError:
            return None

    @staticmethod
    def remove_card_from_reserved(player, reserved_i):
        return player._replace(
            reserved=(player.reserved[0:reserved_i] + player.reserved[reserved_i + 1:]))


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

    return random.Random(seed).sample(all_cards, len(all_cards))

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
    return random.Random(seed).sample(all_cards, len(all_cards))

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

    return random.Random(seed).sample(all_cards, len(all_cards))

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

    return random.Random(seed).sample(all_cards, len(all_cards))

class Tabletop(NamedTuple):
    nobles_deck: tuple
    decks: tuple

    bank: Bank
    players: tuple
    turn: int = 0

    @staticmethod
    def replace_player(tabletop, player_i: int, player: Player):
        new_players = (
            tabletop.players[0:player_i] +
            (player,) +
            tabletop.players[player_i + 1:])
        return tabletop._replace(players=new_players)

    @staticmethod
    def remove_noble_from_deck(tabletop, noble_i: int):
        return tabletop._replace(
            nobles_deck=(tabletop.nobles_deck[0:noble_i] +
                         tabletop.nobles_deck[noble_i + 1:]))

    @staticmethod
    def remove_card_from_deck(tabletop, tier, card_i):
        new_deck = (
            tabletop.decks[tier][0:card_i] +
            tabletop.decks[tier][card_i + 1:])

        new_decks = (
            tabletop.decks[0:tier] +
            (new_deck, ) +
            tabletop.decks[tier + 1:])

        return tabletop._replace(decks=new_decks)

    @staticmethod
    def get_card(tabletop, tier, card_i):
        try:
            return tabletop.decks[tier][card_i]
        except IndexError:
            return False

    @staticmethod
    def setup_game(seed=0, players=4):
        gem_count = 7
        if players == 3:
            gem_count = 5
        elif players == 2:
            gem_count = 4

        return Tabletop(
            nobles_deck=nobles_deck(seed=seed),
            decks=(
                tier_0_deck(seed=seed),
                tier_1_deck(seed=seed),
                tier_2_deck(seed=seed)),
            bank=Bank(
                gold=5,
                diamond=gem_count,
                sapphire=gem_count,
                emerald=gem_count,
                ruby=gem_count,
                onyx=gem_count),
            players=(Player(),) * players)
