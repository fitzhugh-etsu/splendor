from typing import NamedTuple

from .gems import Gems
from .player import Player


class Noble(NamedTuple):
    points: int
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
