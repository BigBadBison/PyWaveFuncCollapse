import os.path

from PIL import Image

from tile import Tile
from tile_generator import TileGenerator

singles = [
    ['test_cross.png', ((0, 0, 0, 0), )],
    ['test_dot.png', ((1, 1, 1, 1), )],
    ['test_blank.png', ((1, 1, 1, 1), )],
    ['test_line.png', ((1, 0, 1, 0), (0, 1, 0, 1))],
    ['test_t.png', ((0, 0, 1, 0), (0, 0, 0, 1), (1, 0, 0, 0), (0, 1, 0, 0))],
]


def test_edges():
    for filename, edges in singles:
        im = Image.open(os.path.join('img', filename)).convert('L')
        tile = Tile(im)
        assert tile.edges == edges[0]


def test_variants():
    for filename, edges in singles:
        tiles = TileGenerator.load(os.path.join('img', filename), 20)
        assert len(tiles) == len(edges)
        print(set([tile.edges for tile in tiles]), set(edges))
        assert set([tile.edges for tile in tiles]) == set(edges)

