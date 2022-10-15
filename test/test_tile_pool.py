from tile import Tile
from tile_pool import TilePool


def test_load():
    pool = TilePool()
    pool.load('img/plotter_wfc_1.png', 20, variants=True, duplicates=False)
    assert len(pool.tiles) == 17


def test_filter():
    pool = TilePool()
    edges = [[1, 1, 1, 1], [0, 0, 0, 0]]
    test_tiles = [Tile(None, e) for e in edges]
    pool.add_tiles(test_tiles)
    filtered = pool.filter_pool(((0, 1), (0, 1), (0, 1), (0, 1)))
    assert len(filtered) == 2
    filtered = pool.filter_pool(((0,), (0, 1), (0, 1), (0, 1)))
    assert len(filtered) == 1 and test_tiles[1] in filtered
    filtered = pool.filter_pool(((0,), (1,), (0, 1), (0, 1)))
    assert len(filtered) == 0
    filtered = pool.filter_pool(((0,), (0,), (0,), (0,)))
    assert len(filtered) == 1 and test_tiles[1] in filtered
    filtered = pool.filter_pool(((1,), (1,), (1,), (1,)))
    assert len(filtered) == 1 and test_tiles[0] in filtered
