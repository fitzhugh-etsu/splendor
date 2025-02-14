from typing import NamedTuple

from .gems import Gems
from .player import Player


class Noble(NamedTuple):
    points: int = 0
    cost: Gems = Gems()

    def __str__(self):
        return f"Cost: {self.cost} Points: {self.points}"

    @staticmethod
    def to_inputs(noble):
        return (noble.points,) + Gems.to_inputs(noble.cost)

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
