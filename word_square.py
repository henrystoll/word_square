import math
import re
import string
from random import randint, randrange, choice

from PIL import Image, ImageDraw, ImageFont, ImageEnhance, ImageColor
from pydantic.dataclasses import dataclass
from typing import List

EMPTY = '.'


@dataclass
class TextVariant:
    header: str
    sub_header: str


def gen_row(size):
    return [EMPTY for _ in range(size)]


def fill_empty(character):
    if character == EMPTY:
        return choice(string.ascii_lowercase)
    else:
        return character


def fill_grid(grid):
    return [list(map(fill_empty, row)) for row in grid]


def print_grid(grid):
    print('\n'.join([' '.join(row) for row in grid]))


def print_line(size):
    [print('-', end='-') for _ in range(size)]
    print()


def generate_word_grid(size: int, words: List[str]):
    grid = [gen_row(size) for _ in range(size)]

    for word in words:
        # rows
        while True:
            if randint(0, 1) == 0:
                grid = list(map(list, zip(*grid)))  # transposes grid 50% of the time

            column = randrange(size)
            row_start = randint(0, size - len(word))

            row_to_change = grid[column][row_start:row_start + len(word)]
            if all(map(lambda char: char == EMPTY, row_to_change)):
                for i, c in enumerate(word):
                    grid[column][row_start + i] = c
                break
            print("trying new combination")

    grid = fill_grid(grid)

    print_line(size)
    return grid


def calc_spacing(font_size):
    return font_size * 0.3


def calc_font(text, font_path, margin, width, draw):
    font_size = 10
    spacing_factor = 0
    while True:
        font = ImageFont.truetype(font_path, font_size)
        text_width, text_height = draw.multiline_textsize(text, font, spacing=font_size * spacing_factor)
        if text_width + margin >= width:
            print(font_size)
            if '\n' in text:
                break
            else:
                return font, text_width, text_height, spacing_factor
        font_size += 1

    # calculate spacing
    while True:
        font = ImageFont.truetype(font_path, font_size)
        text_width, text_height = draw.multiline_textsize(text, font, spacing=font_size * spacing_factor)
        if text_height >= text_width:
            return font, text_width, text_height, spacing_factor
        spacing_factor += 0.005


def get_color(color: str) -> tuple:
    custom_colors = {
        'TRANSPARENT': (0, 0, 0, 0),
        'DARK_WHITE': (255, 255, 255, 180),
    }

    regex_is_custom_color = r"custom\(([_A-Z]+)\)"
    custom = re.match(regex_is_custom_color, color)

    if custom and custom.groups()[0] in custom_colors:
        return custom_colors[custom.groups()[0]]
    else:
        return ImageColor.getrgb(color)


def generate_poster(words: List[str],
                    background=None,
                    grid_size=20,
                    no_columns=4,
                    paper='DIN_A3',
                    resolution=300,
                    margin_height_percent=10,
                    variant='en-1',
                    bg_color_str="#000",
                    text_color_str="custom(DARK_WHITE)",
                    font_header_path='/fonts/Didot.ttc',
                    font_mono_path='/fonts/Menlo.ttc'
                    ) -> Image:
    word_grid = generate_word_grid(grid_size, words)

    # Setup paper and resolution
    papers_dict = {
        'DIN_A3': {
            72: (842, 1191),
            300: (3508, 4961)
        }
    }

    image_size = papers_dict[paper][resolution]

    # Calculate margin based off height
    margin = round(image_size[0] * margin_height_percent * 0.01)

    # Setup header variants
    headers = {
        'en-1': TextVariant("FORGOT YOUR PHONE?", "WORD LIST:"),
        'test-short': TextVariant("test!", "test:"),
        'test-long': TextVariant("test but very ambitious long!", "test but very very long:"),
    }

    # Setup colors
    bg_color = get_color(bg_color_str)
    text_color = get_color(text_color_str)

    # Create Image
    mode = 'RGBA' if len(bg_color) == 4 else "RGB"
    img = Image.new(mode, image_size, color=bg_color)
    width, height = img.size

    draw = ImageDraw.Draw(img)

    # draw header
    text = headers[variant].header

    font, text_width, text_height, _ = calc_font(text, font_header_path, 2 * margin, width, draw)

    current_y = margin
    draw.text(((width - text_width) // 2, current_y), text, font=font, fill=text_color)
    current_y += text_height

    # draw divider
    margin_divider = margin // 3
    width_divider = 20

    current_y += margin_divider
    draw.line((margin, current_y, width - margin, current_y), fill=text_color, width=width_divider)
    current_y += width_divider // 2

    # draw grid
    current_y += margin_divider
    text = '\n'.join([' '.join(row) for row in word_grid])
    font, text_width, text_height, spacing_factor = calc_font(text, font_mono_path, 2 * margin, width, draw)

    draw.multiline_text(((width - text_width) // 2, current_y), text, font=font, fill=text_color,
                        spacing=font.size * spacing_factor)
    current_y += text_height

    # draw sub header
    current_y += margin_divider
    margin_sub_header = 2 * margin + (width - 2 * margin) // 3 * 2

    text = headers[variant].header
    font, text_width, text_height, _ = calc_font(text, font_header_path, margin_sub_header, width, draw)
    text_start_x = (width - text_width) // 2
    draw.multiline_text((text_start_x, current_y), text, font=font, fill=text_color)

    # draw dividers
    current_y += text_height // 2 + width_divider
    draw.line((margin, current_y, text_start_x - margin_divider, current_y), fill=text_color, width=width_divider // 2)
    draw.line((text_start_x + text_width + margin_divider, current_y, width - margin, current_y), fill=text_color,
              width=width_divider // 2)

    # draw word list
    current_y += text_height

    no_rows = math.ceil(len(words) / no_columns)

    width_column = (width - 2 * margin) // no_columns

    split_words = ['\n'.join(words[i: i + no_rows]) for i in range(0, len(words), no_rows)]

    font_size = 10
    spacing_factor = 0.78
    while True:
        font = ImageFont.truetype(font_mono_path, font_size)
        text_width, text_height = draw.multiline_textsize(split_words[0], font, spacing=font_size * spacing_factor)
        if current_y + text_height + margin >= height:
            print(font_size)
            break
        font_size += 1

    for index, text in enumerate(split_words):
        draw.multiline_text((margin + index * width_column, current_y), text, font=font, fill=text_color,
                            spacing=font_size * spacing_factor)

    if background:
        bg = Image.open(f"backgrounds/{background}.jpg")
        bg = bg.resize(image_size)

        bg = ImageEnhance.Brightness(bg).enhance(0.7)
        bg = ImageEnhance.Contrast(bg).enhance(0.7)

        bg.paste(img, (0, 0), img)
        img = bg

    return img

# Save image
# img.save(f"posters/{words[0]}_{size}_{paper}_{resolution}.png")
# img.save(f"posters/{text_file}_{size}_{paper}_{resolution}_{bg_file}.png")
