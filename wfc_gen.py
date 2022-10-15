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
        img = Image.new('L', size)
        for y in range(len(grid)):
            for x in range(len(grid[0])):
                img.paste(im=grid[y][x].im, box=(x * w, y * h))
        img.show()

    def solve_image(self, src) -> None:
        self.q_grid.solve_min()
    #
    # def show_src(self) -> None:
    #     Image.open(self.src).show()
    #
    # def show_blocked(self) -> None:
    #     self.blocked_img.resize(self.img_pixels[0], self.img_pixels[1]).show()
    #

    def show(self) -> None:
        pass


if __name__ == '__main__':
    image_src = 'img/dog-nose.jpg'
    tile_pixels = 20
    size = (297, 420)
    print('creating converter...')
    wfc_converter = WFCConverter(size)
    print('loading...')
    wfc_converter.load_tiles('img/plotter_wfc_1.png', tile_pixels)
    print('solving...')
    wfc_converter.solve_random()

    print('solved!')
    wfc_converter.show()
    print(wfc_converter.q_grid.pool.filter_pool.cache_info())
    print(wfc_converter.q_grid.pool._filter_edge.cache_info())
    print(wfc_converter.q_grid.pool.filter_edges.cache_info())
