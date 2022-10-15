from tile import Direction, Tile
from tile_pool import TilePool, PoolGenerator


class TestTile:
    def __init__(self, edges):
        self.edges = edges

    def __repr__(self):
        return f'<TestTile {self.edges}>'


def test_pool_generator():
    tiles = PoolGenerator.load('img/plotter_wfc_1.png', 20)
    i = 0
    for t in tiles:
        print(t.edges)
        i += 1
        t.im.save(str(i) + '.png')
    assert False


def test_load():
    pool = TilePool()
    pool.load('img/plotter_wfc_1.png', 20)
    assert len(pool.tiles) == 17


def test_edge_pool():
    pool = TilePool()
    pool.load('img/plotter_wfc_1.png', 20)
    for d in Direction:
        for e in Tile.edge_types:
            assert all(tile.edges[d] == e for tile in pool.edge_pools[d][e])
        assert sum(len(edge_pool) for edge_pool in pool.edge_pools[d]) == len(pool.tiles)
        assert set(t for edge_pool in pool.edge_pools[d] for t in edge_pool) == set(pool.tiles)


def test_filter():
    pool = TilePool()
    edges = [[1, 1, 1, 1], [0, 0, 0, 0]]
    test_tiles = [TestTile(e) for e in edges]
    pool.add_tiles(test_tiles)
    filtered = pool.filter_pool((0, 1), (0, 1), (0, 1), (0, 1))
    assert len(filtered) == 2
    filtered = pool.filter_pool((0,), (0, 1), (0, 1), (0, 1))
    assert len(filtered) == 1 and filtered[0] == test_tiles[1]
    filtered = pool.filter_pool((0,), (1,), (0, 1), (0, 1))
    assert len(filtered) == 0
    filtered = pool.filter_pool((0,), (0,), (0,), (0,))
    assert len(filtered) == 1 and filtered[0] == test_tiles[1]
    filtered = pool.filter_pool((1,), (1,), (1,), (1,))
    assert len(filtered) == 1 and filtered[0] == test_tiles[0]
