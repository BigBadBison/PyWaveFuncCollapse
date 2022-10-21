import random
from typing import Callable

from PIL import Image

from quantum_tile import QuantumTile, InvalidLayoutError
from tile import Direction, Tile
from tile_pool import TilePool


class QuantumGrid:
    def __init__(self, pool: TilePool, size: tuple[int, int]):
        self.size = size
        self.pool = pool
        self.quantum_grid = self._create_quantum_grid()

    def _create_quantum_grid(self) -> list[list[QuantumTile]]:
        q_grid = []
        for y in range(self.size[1]):
            q_grid.append([])
            for x in range(self.size[0]):
                qt = QuantumTile((x, y), self.pool)  # set value here
                q_grid[y].append(qt)
                if y > 0:
                    qt.set_neighbor(Direction.N, q_grid[y - 1][x])
                if x > 0:
                    qt.set_neighbor(Direction.W, q_grid[y][x - 1])
        return q_grid

    def _create_tile_grid(self):
        grid = []
        for row in self.quantum_grid:
            grid.append([None for _ in row])
        return grid

    def solve_random(self, seed=1) -> list[list[Tile]]:
        return self.solve(lambda tile: tile.set_random(), seed)

    def solve_target(self, targets: list[list[tuple[int, int, int]]], seed=1, noise=0) -> list[list[Tile]]:
        self.set_targets(targets)
        return self.solve(lambda tile: tile.set_closest(noise=noise), seed)

    def set_targets(self, targets: list[list[tuple[int, int, int]]]):
        for q_tile, targ in zip(self, targets):
            q_tile.value = targ

    def solve(self, strategy: Callable, seed=1) -> list[list[Tile]]:
        self._initialize()
        grid = self._create_tile_grid()
        dirty_tiles = set()
        tile_seq = [tile for tile in self]
        random.seed(seed)
        random.shuffle(tile_seq)
        i = 0
        while tile_seq:
            i += 1
            q_tile = tile_seq.pop()
            try:
                tile = strategy(q_tile)
                grid[q_tile.y][q_tile.x] = tile
                dirty_tiles.update(q_tile.get_dirty_neighbors())
                while dirty_tiles:
                    dirty_tile = dirty_tiles.pop()
                    dirty_tile.update_edges()
                    dirty_tiles.update(dirty_tile.get_dirty_neighbors())
            except InvalidLayoutError:
                raise
            if not i % 10000:
                print(f'solving: {(i * 100) // (self.size[0] * self.size[1])}%')
        return grid

    def _initialize(self):
        if not self.pool.is_complete():
            missing = self.pool.get_missing_combinations()
            print(f'WARNING: {len(missing)} edge combinations missing, invalid layout possible!')
        for tile in self:
            tile.initialize()

    def __iter__(self):
        for row in self.quantum_grid:
            for tile in row:
                yield tile
