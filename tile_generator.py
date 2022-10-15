from PIL import Image, ImageOps, ImageChops

from tile import Tile


class TileGenerator:
    def __init__(self):
        self._edge_type_vals = []

    @property
    def edge_types(self) -> tuple[int, ...]:
        return tuple(i for i in range(len(self._edge_type_vals)))

    @property
    def edge_count(self) -> int:
        return len(self._edge_type_vals)

    def load(self, src, size, variants=True, duplicates=True) -> list[Tile]:
        im = Image.open(src)
        images = self._split_image(im, size)
        if variants:
            images = self._create_variants(images)
        if not duplicates:
            images = self._remove_duplicates(images, 7500)
        tiles = self._create_tiles(images)
        return tiles

    def _split_image(self, im, size) -> list[Image]:
        sub_images = []
        for x in range(0, im.width, size):
            for y in range(0, im.height, size):
                box = (x, y, x + size, y + size)
                image = im.crop(box)
                sub_images.append(image)
        return sub_images

    def _create_variants(self, images: list[Image]) -> list[Image]:
        img_in = list(images) + [ImageOps.flip(tile) for tile in list(images)]
        img_out = list(img_in)
        for im in img_in:
            for i in range(1, 4):
                im = im.rotate(i * 90)
                img_out.append(im)
        return img_out

    def _remove_duplicates(self, images: list[Image], tol) -> list[Image]:
        img_out = []
        for new_img in images:
            for existing_img in img_out:
                diff = ImageChops.difference(new_img, existing_img)
                sum_diff = sum(diff.getdata())
                if sum_diff <= tol:
                    break
            else:
                img_out.append(new_img)
        return img_out

    def _create_tiles(self, images) -> list[Tile]:
        return [self._create_tile(im) for im in images]

    def _create_tile(self, image: Image) -> Tile:
        edges = []
        mid = (image.width * 0.5, image.height * 0.5)
        for e in ((mid[0], 2), (image.width - 2, mid[1]), (mid[0], image.height - 2), (2, mid[1])):
            val = image.getpixel(e)
            if val not in self._edge_type_vals:
                self._edge_type_vals.append(val)
            edges.append(self._edge_type_vals.index(val))
        return Tile(image, edges)
