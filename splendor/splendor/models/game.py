import random
from typing import NamedTuple

from . import decks as decks
from .bank import Bank
from .player import Player


class Game(NamedTuple):
    nobles_deck: tuple
    decks: tuple

    bank: Bank
    players: tuple
    turn: int = 0

    @staticmethod
    def replace_player(game, player_i: int, player: Player):
        new_players = (
            game.players[0:player_i] +
            (player,) +
            game.players[player_i + 1:])
        return game._replace(players=new_players)

    @staticmethod
    def remove_noble_from_deck(game, noble_i: int):
        return game._replace(
            nobles_deck=(game.nobles_deck[0:noble_i] +
                         game.nobles_deck[noble_i + 1:]))

    @staticmethod
    def remove_card_from_deck(game, tier, card_i):
        new_deck = (
            game.decks[tier][0:card_i] +
            game.decks[tier][card_i + 1:])

        new_decks = (
            game.decks[0:tier] +
            (new_deck, ) +
            game.decks[tier + 1:])

        return game._replace(decks=new_decks)

    @staticmethod
    def get_card(game, tier, card_i):
        try:
            return game.decks[tier][card_i]
        except IndexError:
            return False

    def __str__(game):
        tiers = ''
        for i in range(len(game.decks)):
            tiers += f"\nT{i}:\n" + "\n".join([" " + str(card) for card in game.decks[i][0:4]])

        players = "\n".join(["Player\n" + str(player) for player in game.players])

        return f"""
Bank: {game.bank}
{tiers}
Player: {game.turn % len(game.players)}
{players}
            """

    @staticmethod
    def setup_game(seed=None, players=4):
        gem_count = 7
        if players == 3:
            gem_count = 5
        elif players == 2:
            gem_count = 4

        return Game(
            nobles_deck=decks.nobles_deck(seed=seed),
            decks=(
                decks.tier_0_deck(seed=seed),
                decks.tier_1_deck(seed=seed),
                decks.tier_2_deck(seed=seed)),
            bank=Bank(
                gold=5,
                diamond=gem_count,
                sapphire=gem_count,
                emerald=gem_count,
                ruby=gem_count,
                onyx=gem_count),
            players=(Player(),) * players)
