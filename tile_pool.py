import itertools
import math
import random
import typing
import functools

from PIL import Image

from tile import Tile, Direction
from tile_generator import TileGenerator


class TilePool:
    def __init__(self):
        self.generator = TileGenerator()
        self.tiles: list[Tile] = []

    @property
    def tile_size(self):
        try:
            return self.tiles[0].im.size
        except IndexError:
            return 0

    def load(self, src, size, variants=True, duplicates=True):
        tiles = self.generator.load(src, size, allow_mirror=variants, allow_rotate=variants,
                                    allow_duplicates=duplicates)
        self.add_tiles(tiles)

    def add_tiles(self, tiles: typing.List[Tile]):
        self.get_tiles_with_edge_in_direction.cache_clear()
        self.get_tiles_with_edges_in_direction.cache_clear()
        self.filter_pool.cache_clear()
        self.filter_edges.cache_clear()
        self.tiles += tiles

    def get_random(self, edges: tuple[tuple[int, ...], ...]) -> Tile:
        return random.choice([i for i in self.filter_pool(edges)])

    def get_closest(self, edges: tuple[tuple[int, ...], ...], value: tuple[int, int, int], noise=0) -> Tile:
        tiles = self.filter_pool(edges)
        return min((tile.difference(value, noise=noise), tile) for tile in tiles)[1]

    def get_initial_edges(self) -> tuple[tuple[int, ...], ...]:
        return self.filter_edges(tuple(tuple(e for e in self.generator.edge_types) for _ in Direction))

    @functools.lru_cache(maxsize=None)
    def get_tiles_with_edge_in_direction(self, d: Direction, edge_type: int) -> set[Tile]:
        return {tile for tile in self.tiles if tile.edges[d] == edge_type}

    @functools.lru_cache(maxsize=None)
    def get_tiles_with_edges_in_direction(self, d: Direction, edge_types: tuple[int]) -> set[Tile]:
        tiles = set()
        for edge_type in edge_types:
            tiles = tiles.union(self.get_tiles_with_edge_in_direction(d, edge_type))
        return tiles

    @functools.lru_cache(maxsize=None)
    def filter_pool(self, edges: tuple[tuple[int, ...], ...]) -> set[
        Tile]:
        tiles = {t for t in self.tiles}
        for d, edge_types in zip(Direction, edges):
            tiles = tiles.intersection(self.get_tiles_with_edges_in_direction(d, edge_types))
        return tiles

    @functools.lru_cache(maxsize=None)
    def filter_edges(self, edges: tuple[tuple[int, ...], ...]) -> tuple[tuple[int, ...], ...]:
        pool = self.filter_pool(edges)
        edges = [set() for _ in Direction]
        for tile in pool:
            for i, edge in enumerate(tile.edges):
                edges[i].add(edge)
        return tuple(tuple(edge) for edge in edges)

    def is_complete(self) -> bool:
        return len(self.get_missing_combinations()) == 0

    def get_missing_combinations(self):
        missing = []
        edge_types = [(e,) for e in self.generator.edge_types]
        for edges in itertools.product(edge_types, repeat=len(Direction)):
            if len(self.filter_pool(edges)) == 0:
                missing.append(edges)
        return missing

    def show(self) -> None:
        w = len(self) * self.tiles[0].im.width
        h = self.tiles[0].im.height
        img = Image.new('RGB', (w, h))
        x = 0
        for tile in self.tiles:
            img.paste(im=tile.im, box=(x, 0))
            x += tile.im.width
        img.show()

    def show_square(self) -> None:
        w = int(math.sqrt(len(self))) * self.tiles[0].im.width
        h = w + self.tiles[0].im.width
        img = Image.new('RGB', (w, h))
        i = 0
        for y in range(0, h, self.tiles[0].im.height):
            for x in range(0, w, self.tiles[0].im.width):
                try:
                    img.paste(im=self.tiles[i].im, box=(x, y))
                except IndexError:
                    img.show()
                    return
                i += 1
        img.show()

    def __len__(self):
        return len(self.tiles)
