import os.path
from tile_generator import TileGenerator

singles = [
    ['test_cross.png', ((0, 0, 0, 0), )],
    ['test_dot.png', ((0, 0, 0, 0), )],
    ['test_blank.png', ((0, 0, 0, 0), )],
    ['test_line.png', ((0, 1, 0, 1), (1, 0, 1, 0))],
    ['test_t.png', ((0, 0, 1, 0), (0, 0, 0, 1), (1, 0, 0, 0), (0, 1, 0, 0))],
]


def test_load():
    for filename, edges in singles:
        generator = TileGenerator()
        tiles = generator.load(os.path.join('img', filename), 20, allow_mirror=False, allow_rotate=False)
        assert len(tiles) == 1
        assert tiles[0].edges == edges[0]
        assert generator.edge_count == max(edges[0]) + 1


def test_rotate():
    for filename, edges in singles:
        generator = TileGenerator()
        tiles = generator.load(os.path.join('img', filename), 20, allow_mirror=False, allow_rotate=True, allow_duplicates=True)
        assert len(tiles) == 4


def test_mirror_and_rotate():
    for filename, edges in singles:
        generator = TileGenerator()
        tiles = generator.load(os.path.join('img', filename), 20, allow_mirror=True, allow_rotate=True, allow_duplicates=True)
        assert len(tiles) == 8


def test_duplicates():
    for filename, edges in singles:
        generator = TileGenerator()
        tiles = generator.load(os.path.join('img', filename), 20, allow_mirror=True, allow_rotate=True, allow_duplicates=False)
        assert len(tiles) == len(edges)
        assert set([tile.edges for tile in tiles]) == set(edges)


def test_test_set():
    generator = TileGenerator()
    tiles = generator.load('img/plotter_wfc_1.png', 20, allow_mirror=True, allow_rotate=True, allow_duplicates=False)
    assert len(tiles) == 17
