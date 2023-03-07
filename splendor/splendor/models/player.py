from itertools import zip_longest
from typing import NamedTuple

from .. import defs as d
from .bank import Bank
from .card import Card
from .gems import Gems


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
    def is_turn(game, player_i):
        return (game.turn % len(game.players)) == player_i

    @staticmethod
    def points(player):
        return sum([n.points for n in player.nobles]) + \
            sum([c.points for c in player.purchased])

    @staticmethod
    def add_gems(player, gems):
        return player._replace(
            bank=Bank.add_gems(
                player.bank,
                gems))

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
    def add_card_to_reserved(player, card, hidden=False):
        return player._replace(
            reserved=((card._replace(hidden=hidden),) + player.reserved))

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

    @staticmethod
    def to_inputs(player, is_current_player=False):
        inputs = []
        inputs.extend(Bank.to_inputs(player.bank))
        inputs.extend(Gems.to_inputs(Player.get_bonus(player)))
        inputs.append(Player.points(player))

        # Reserved
        for (i, reserved_card) in zip_longest(
                range(3),
                player.reserved[0:3],
                fillvalue=Card()):
            inputs.extend(Card.to_inputs(reserved_card, hidden=not is_current_player))

        return inputs
