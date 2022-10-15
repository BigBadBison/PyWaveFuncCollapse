import random

from quantum_tile import QuantumTile, InvalidLayoutError
from tile import Direction
from tile_pool import TilePool


class QuantumGrid:
    def __init__(self, size: tuple[int, int]):
        self.size = size
        self.pool = TilePool()
        self.quantum_grid = self._create_quantum_grid()

    def _create_quantum_grid(self) -> list[list[QuantumTile]]:
        q_grid = []
        for y in range(self.size[1]):
            q_grid.append([])
            for x in range(self.size[0]):
                qt = QuantumTile(self.pool)
                q_grid[y].append(qt)
                if y > 0:
                    qt.set_neighbor(Direction.N, q_grid[y - 1][x])
                if x > 0:
                    qt.set_neighbor(Direction.W, q_grid[y][x - 1])
        return q_grid

    def create_grid(self):
        grid = []
        for row in self.quantum_grid:
            grid.append([])
            for cell in row:
                tile = cell.tile_pool.get_random(cell.edges)
                grid[-1].append(tile)
        return grid

    def load(self, src: str, size: int):
        self.pool.load(src, size)

    def solve_random(self, seed=1):
        random.seed(seed)
        # print({d: p for d, p in zip(Direction, self.pool.edge_pools)})
        self._initialize_tiles()
        dirty_tiles = set()
        tile_seq = [tile for tile in self]
        random.shuffle(tile_seq)
        i = 0
        while tile_seq:

            tile = tile_seq.pop()
            i += 1
            if tile.assigned:
                continue
            try:
                dirty = tile.set_random()
                dirty_tiles.update(dirty)
                while dirty_tiles:
                    dirty_tile = dirty_tiles.pop()
                    dirty_tile.update_edges()
                    dirty_tiles.update(dirty_tile.get_dirty_neighbors())
            except InvalidLayoutError:
                print('invalid layout')
                raise
            if not i % 10000:
                print(f'i: {i}')
        return self.create_grid()

    def solve_min(self):
        tile_seq = [cell for row in self.quantum_grid for cell in row]
        random.shuffle(tile_seq)
        i = 0
        while tile_seq:
            # NOT POPPING FROM TILE_SEQ, MIN IS VERY SLOW. TRACK MIN WHILE UPDATING?
            tile = min((i for i in tile_seq if i.valid_tile_count > 1), key=lambda x: x.valid_tile_count)
            i += 1
            if not i % 1000:
                print(f'i: {i}, len: {len(tile.valid_tile_count)}')
            if tile.assigned:
                continue
            try:
                tile.set_tile_from_pool()
            except RecursionError:
                print('recursion error')
            except InvalidLayoutError:
                print('invalid layout')

    def _initialize_tiles(self):
        for tile in self:
            tile.initialize()

    def __iter__(self):
        for row in self.quantum_grid:
            for tile in row:
                yield tile
