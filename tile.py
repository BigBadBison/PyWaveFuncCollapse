import enum
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
    def __init__(self, im: Image, edges: typing.Iterable[int]):
        self.im = im
        self.edges = tuple(edges)

    def show(self):
        self.im.show()

    def __repr__(self):
        return f'<Tile {self.edges}>'
