import enum
import random
import typing

from PIL import Image


class Direction(enum.IntEnum):
    N = 0
    E = 1
    S = 2
    W = 3

    @classmethod
    def opposite(cls, direction: 'Direction'):
        return [d for d in Direction][direction - 2]


class Tile:
    def __init__(self, im: Image, edges: typing.Iterable[int], value=(0, 0, 0)):
        self.im = im
        self.value = value
        self.edges = tuple(edges)

    def show(self):
        self.im.show()

    def difference(self, value: tuple[int, int, int], noise=0) -> int:
        return sum(abs(i + random.uniform(-noise, noise) - j) for i, j in zip(self.value, value))

    def __repr__(self):
        return f'<Tile {self.edges}>'

    def __lt__(self, other):
        return self.value < other.value
