# Import required Image library
from dataclasses import dataclass
from random import choice

from PIL import Image


@dataclass
class Background:
    file: str
    offset: tuple
    size: tuple


poster_file = "barnacle_20_DIN_A3_300"

backgrounds = [
    Background("01", (537, 699), (1115, 1590)),
    Background("02", (1376, 2438), (760, 1025)),
    Background("03", (1100, 395), (688, 940)),
    Background("04", (2024, 552), (1252, 1812)),
    Background("05", (1575, 535), (598, 842)),

]

for selected in backgrounds:
    # selected = choice(backgrounds)
    # selected = backgrounds[4]
    # Create an Image Object from an Image
    bg = Image.open(f"backgrounds/{selected.file}.jpg")
    img = Image.open(f"posters/{poster_file}.png")
    # Display actual image
    # bg.show()
    # img.show()

    # Make the new image half the width and half the height of the original image
    img = img.resize(selected.size)
    bg.paste(img, selected.offset)

    # Display the resized imaged
    # bg.show()

    bg.save(f"posters/{poster_file}_{selected.file}.jpg")
