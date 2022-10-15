from quantum_tile import QuantumTile
from tile import Tile, Direction
from tile_pool import TilePool


class TestTile:
    def __init__(self, edges):
        self.edges = edges

    def __repr__(self):
        return f'<TestTile {self.edges}>'


def test_set_tile():
    pool = TilePool()
    edges = [[1,0,0,0], [1,1,1,1], [0,0,0,0]]
    pool.add_tiles([TestTile(e) for e in edges])
    qt = QuantumTile(pool)
    neighbors = [QuantumTile(pool) for _ in Direction]
    for d, n in zip(Direction, neighbors):
        qt.set_neighbor(d, n)
