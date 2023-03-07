from typing import NamedTuple


class Gems(NamedTuple):
    diamond: int = 0
    sapphire: int = 0
    emerald: int = 0
    ruby: int = 0
    onyx: int = 0

    @staticmethod
    def to_inputs(gems):
        return tuple([v for v in gems])

    @staticmethod
    def subtract(g1, g2, allow_negative=True):
        if allow_negative:
            return Gems(*[g1[i] - g2[i] for i in range(len(Gems()))])
        else:
            return Gems(*[max(0, g1[i] - g2[i]) for i in range(len(Gems()))])

    @staticmethod
    def add(g1, g2, allow_negative=True):
        return Gems(*[g1[i] + g2[i] for i in range(len(Gems()))])

    def __str__(self):
        return f"{self.diamond}D {self.sapphire}S {self.emerald}E {self.ruby}R {self.onyx}O"
