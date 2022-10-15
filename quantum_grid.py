import random

from PIL import Image

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
                qt = QuantumTile((x, y), self.pool)
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
                # print(cell.edges)
                tile = cell.tile_pool.get_random(cell.edges)
                grid[-1].append(tile)
        return grid

    def load(self, src: str, size: int):
        self.pool.load(src, size)

    def solve_random(self, seed=1):
        if not self.pool.is_complete():
            missing = self.pool.get_missing_combinations()
            print(f'WARNING: {len(missing)} edge combinations missing, invalid layout possible!')
        self._initialize_tiles()
        dirty_tiles = set()
        tile_seq = [tile for tile in self]
        random.seed(seed)
        random.shuffle(tile_seq)
        while tile_seq:
            tile = tile_seq.pop()
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
                raise
        return self.create_grid()

    def solve_image(self, src, seed=1):
        img = Image.open(src)
        img = img.resize(self.size)
        if not self.pool.is_complete():
            missing = self.pool.get_missing_combinations()
            print(f'WARNING: {len(missing)} edge combinations missing, invalid layout possible!')
        self._initialize_tiles()
        dirty_tiles = set()
        tile_seq = [tile for tile in self]
        random.seed(seed)
        random.shuffle(tile_seq)
        i = 0
        while tile_seq:
            i += 1
            tile = tile_seq.pop()
            if tile.assigned:
                continue
            try:
                dirty = tile.set_closest(img.getpixel(tile.pos))
                dirty_tiles.update(dirty)
                while dirty_tiles:
                    dirty_tile = dirty_tiles.pop()
                    dirty_tile.update_edges()
                    dirty_tiles.update(dirty_tile.get_dirty_neighbors())
            except InvalidLayoutError:
                raise
            if not i % 10000:
                print(f'i: {i}')
        return self.create_grid()

    def _initialize_tiles(self):
        for tile in self:
            tile.initialize()

    def __iter__(self):
        for row in self.quantum_grid:
            for tile in row:
                yield tile
