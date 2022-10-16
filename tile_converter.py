from PIL import Image

image_src = 'img/plotter_wfc_1.png'


def pixellate(img: Image):
    img_small = img.resize((16, 16), resample=Image.BILINEAR)
    result = img_small.resize(img.max_size, Image.NEAREST)
    return result


img_ = Image.open(image_src).convert('L')
img_ = pixellate(img_)
