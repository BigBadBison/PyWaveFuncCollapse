import random
import typing
import functools

from PIL import Image, ImageOps, ImageChops

from tile import Tile, Direction


class TilePool:
    def __init__(self):
        self.tiles = []
        self.edge_pools: list[list[[Tile]]] = [[[] for _ in Tile.edge_types] for _ in Direction]

    def load(self, src, size):
        tiles = PoolGenerator.load(src, size)
        self.add_tiles(tiles)

    def add_tiles(self, tiles: typing.List[Tile]):
        for tile in tiles:
            for direction, edge_type in enumerate(tile.edges):
                self.edge_pools[direction][edge_type].append(tile)
            self.tiles.append(tile)

    def get_random(self, edges):
        return random.choice(self.get_valid_tiles(edges))

    def get_valid_tiles(self, edges):
        return self.filter_pool(*edges)

    def get_valid_edges(self, edges):
        return self.filter_edges(*edges)

    @functools.lru_cache(maxsize=None)
    def filter_pool(self, n, e, s, w) -> tuple[Tile, ...]:
        new_pool = set(self._filter_edge(0, n))
        new_pool = new_pool.intersection(self._filter_edge(1, e))
        new_pool = new_pool.intersection(self._filter_edge(2, s))
        new_pool = new_pool.intersection(self._filter_edge(3, w))
        return tuple(new_pool)

    @functools.lru_cache(maxsize=None)
    def _filter_edge(self, i, edges) -> tuple[Tile, ...]:
        pool = set()
        for edge in edges:
            pool.update(self.edge_pools[i][edge])
        return tuple(pool)

    @functools.lru_cache(maxsize=None)
    def filter_edges(self, n, e, s, w):
        pool = self.filter_pool(n, e, s, w)
        edges = [set() for _ in range(4)]
        for tile in pool:
            for i, edge in enumerate(tile.edges):
                edges[i].add(edge)
        return tuple(tuple(edge) for edge in edges)

    def __len__(self):
        return len(self.tiles)


class PoolGenerator:
    @staticmethod
    def load(src, size):
        im = Image.open(src).convert('L')
        images = PoolGenerator.split_image(im, size)
        images = PoolGenerator.create_variants(images)
        tiles = [Tile(im) for im in images]
        return tiles

    @staticmethod
    def split_image(im, size):
        tiles = []
        for x in range(0, im.width, size):
            for y in range(0, im.height, size):
                box = (x, y, x + size, y + size)
                tile = im.crop(box)
                tiles.append(tile)
        return tiles

    @staticmethod
    def create_variants(tiles_in):
        tiles = list(tiles_in) + [ImageOps.flip(tile) for tile in list(tiles_in)]
        tiles_out = list(tiles)
        for tile in tiles:
            for i in range(1, 4):
                new_tile = tile.rotate(i * 90)
                tiles_out.append(new_tile)
        tiles_out = PoolGenerator.remove_duplicates(tiles_out, 7500)
        return tiles_out

    @staticmethod
    def remove_duplicates(tiles_in, tol):
        tiles_out = []
        for new_tile in tiles_in:
            for existing_tile in tiles_out:
                diff = ImageChops.difference(new_tile, existing_tile)
                sum_diff = sum(diff.getdata())
                if sum_diff <= tol:
                    break
            else:
                tiles_out.append(new_tile)
        return tiles_out

# def show_tiles(tiles):
#     count = len(tiles)
#     im = Image.new('L', (count * tile_pixels, tile_pixels))
#     for i in range(count):
#         im.paste(tiles[i].im, (i * tile_pixels, 0))
#     im.show()
