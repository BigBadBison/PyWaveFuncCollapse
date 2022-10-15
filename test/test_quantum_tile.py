from quantum_tile import QuantumTile
from tile import Tile, Direction
from tile_pool import TilePool


def test_set_tile():
    pool = TilePool()
    edges = [[1,0,0,0], [1,1,1,1], [0,0,0,0]]
    pool.add_tiles([Tile(None, e) for e in edges])
    qt = QuantumTile(pool)
    neighbors = [QuantumTile(pool) for _ in Direction]
    for d, n in zip(Direction, neighbors):
        qt.set_neighbor(d, n)
