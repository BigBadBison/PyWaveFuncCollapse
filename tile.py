import enum
import typing
import functools

from PIL import Image, ImageOps, ImageChops


class Direction(enum.IntEnum):
    N = 0
    E = 1
    S = 2
    W = 3

    @classmethod
    def opposite(cls, direction: 'Direction'):
        return [d for d in Direction][direction - 2]


class Tile:
    edge_types = (0, 1)

    def __init__(self, im):
        self.im = im
        self.edges = self._set_edges()

    def _set_edges(self):
        # todo: this goes in pool generator
        edges = []
        midpoint = self.im.width * 0.5
        for e in ((midpoint, 2), (self.im.width - 2, midpoint), (midpoint, self.im.width - 2), (2, midpoint)):
            val = self.im.getpixel(e)
            edges.append(int(bool(val)))
        return tuple(edges)

    def __repr__(self):
        return f'<Tile {self.edges}>'
