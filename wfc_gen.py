from __future__ import annotations

from PIL import Image

from quantum_grid import QuantumGrid


class WFCConverter:
    def __init__(self, max_tiles: [int, int]):
        self.max_tiles = max_tiles
        self.q_grid = QuantumGrid(self.max_tiles)

    def _create_blocked_image(self, src):
        img = Image.open(src).convert('L')
        blocked_img = self.resize(img, self.max_tiles[0], self.max_tiles[1], maintain_aspect=True, resample=Image.BICUBIC)
        return blocked_img

    @staticmethod
    def resize(img: Image.Image, width, height, maintain_aspect=True, resample=None):
        if maintain_aspect:
            ratio = min(width / img.width, height / img.height)
            width = int(img.width * ratio)
            height = int(img.height * ratio)
        return img.resize((width, height), resample=resample)

    def load_tiles(self, src: str, size: int):
        self.q_grid.load(src, size)

    def solve_random(self) -> None:
        grid = self.q_grid.solve_random()
        w, h = grid[0][0].im.size
        size = (w * len(grid[0]), h * len(grid))
        img = Image.new('RGB', size)
        for y in range(len(grid)):
            for x in range(len(grid[0])):
                img.paste(im=grid[y][x].im, box=(x * w, y * h))
        img.show()

    def solve_image(self, src) -> None:
        grid = self.q_grid.solve_image(src)
        w, h = grid[0][0].im.size
        size = (w * len(grid[0]), h * len(grid))
        img = Image.new('RGB', size)
        for y in range(len(grid)):
            for x in range(len(grid[0])):
                img.paste(im=grid[y][x].im, box=(x * w, y * h))
        img.show()

    def show(self) -> None:
        pass


if __name__ == '__main__':
    tile_pixels = 20
    size = (800, 533)
    wfc_converter = WFCConverter(size)
    wfc_converter.load_tiles(r'img/plotter_wfc_1_2_color.png', tile_pixels)
    wfc_converter.solve_image(r'img/trees_bwr.jpg')
    wfc_converter.show()
