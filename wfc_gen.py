from __future__ import annotations

import numpy
from PIL import Image

from quantum_grid import QuantumGrid
from tile import Tile
from tile_pool import TilePool


class WFCConverter:
    def __init__(self, max_tiles: [int, int]):
        self._max_tiles = max_tiles
        self.width, self.height = max_tiles
        self.pool = TilePool()
        self.grid: list[list[Tile]] = []

    @property
    def size(self) -> tuple[int, int]:
        return self.width, self.height

    def load_tiles(self, src: str, size: int):
        self.pool.load(src, size)

    def solve_random(self) -> None:
        q_grid = QuantumGrid(self.pool, self.size)
        self.grid = q_grid.solve_random()

    def solve_image(self, src) -> None:
        img = Image.open(src)
        img = self.resize(img)
        q_grid = QuantumGrid(self.pool, self.size)
        self.grid = q_grid.solve_target(numpy.array(img.getdata()).tolist())

    def resize(self, img: Image.Image):
        ratio = min(self._max_tiles[0] / img.width, self._max_tiles[1] / img.height)
        self.width = int(img.width * ratio)
        self.height = int(img.height * ratio)
        return img.resize((self.width, self.height))

    def show(self) -> None:
        w, h = self.pool.tile_size
        size = (w * self.width, h * self.height)
        img = Image.new('RGB', size)
        for y in range(self.height):
            for x in range(self.width):
                img.paste(im=self.grid[y][x].im, box=(x * w, y * h))
        img.show()


if __name__ == '__main__':
    tile_pixels = 20
    max_size = (800, 533)
    wfc_converter = WFCConverter(max_size)
    wfc_converter.load_tiles(r'img/plotter_wfc_1_2_color.png', tile_pixels)
    wfc_converter.solve_image(r'img/trees_bwr.jpg')
    wfc_converter.show()
