import string
from random import randint, randrange, choice, seed
from PIL import Image, ImageDraw, ImageFont, ImageEnhance

COL = 'col'
ROW = 'row'
EMPTY = '.'


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


def gen_word_grid(size, words):
    grid = [gen_row(size) for _ in range(size)]

    for word in words:
        # rows
        while True:
            if choice([ROW, COL]) == COL:
                grid = list(map(list, zip(*grid)))  # transposes grid

            column = randrange(size)
            row_start = randint(0, size - len(word))

            row_to_change = grid[column][row_start:row_start + len(word)]
            if all(map(lambda c: c == EMPTY, row_to_change)):
                for i, c in enumerate(word):
                    grid[column][row_start + i] = c
                break
            print("trying")

    print_grid(grid)
    grid = fill_grid(grid)
    # print_line(size)
    # print_grid(grid)

    print_line(size)
    return grid


def calc_spacing(font_size):
    return font_size * 0.3


def calc_font(text, font_path, margin):
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


seed("test")

size = 20
paper = 'DIN_A3'
resolution = 300
margin_height_percent = 10


text_file = "camping"
# text_file = "ocean"

with open(f"texts/{text_file}.txt") as file:
    words = file.read().splitlines()


word_grid = gen_word_grid(size, words)

# Setup size and font

papers_dict = {
    'DIN_A3': {
        72: (842, 1191),
        300: (3508, 4961)
    }
}

image_size = papers_dict[paper][resolution]
font_header_path = '/Library/Fonts/Didot.ttc'
# font_header_path = '/Library/Fonts/MarkerFelt.ttc'
font_mono_path = '/Library/Fonts/Menlo.ttc'
# font_mono_path = '/Library/Fonts/Supplemental/Courier New.ttf'
margin = round(image_size[0] * margin_height_percent * 0.01)

# Setup text
header = {'en-1': "FORGOT YOUR PHONE?", 'short': "test", 'long': "very long words and even more text:"}
sub_header = {'en-1': "WORD LIST:", 'short': "test", 'long': "very long words and text:"}
variant = 'en-1'
# variant = 'short'
# variant = 'long'

# Setup colors
TRANSPARENT = (0, 0, 0, 0)
WHITE = (255, 255, 255, 255)
DARK_WHITE = (255, 255, 255, 180)
# DARK_WHITE = (230, 230, 230, 200)
LIGHT_GREY = (200, 200, 200, 255)
DARK_GREY = (50, 50, 50, 255)
BLACK = (0, 0, 0, 255)

bg_color = TRANSPARENT
text_color = DARK_WHITE
# text_color = DARK_GREY

# Create Image
img = Image.new('RGBA', image_size, color=bg_color)
width, height = img.size

draw = ImageDraw.Draw(img)

# draw header
text = header[variant]

font, text_width, text_height, _ = calc_font(text, font_header_path, 2 * margin)

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
font, text_width, text_height, spacing_factor = calc_font(text, font_mono_path, 2 * margin)

draw.multiline_text(((width - text_width) // 2, current_y), text, font=font, fill=text_color,
                    spacing=font.size * spacing_factor)
current_y += text_height

# draw sub header
current_y += margin_divider
margin_sub_header = 2 * margin + (width - 2 * margin) // 3 * 2

text = sub_header[variant]
font, text_width, text_height, _ = calc_font(text, font_header_path, margin_sub_header)
text_start_x = (width - text_width) // 2
draw.multiline_text((text_start_x, current_y), text, font=font, fill=text_color)

# draw dividers
current_y += text_height // 2 + width_divider
draw.line((margin, current_y, text_start_x - margin_divider, current_y), fill=text_color, width=width_divider // 2)
draw.line((text_start_x + text_width + margin_divider, current_y, width - margin, current_y), fill=text_color,
          width=width_divider // 2)

# draw word list
current_y += text_height

no_columns = 4
no_rows = 5

width_column = (width - 2 * margin) // no_columns

split_words = ['\n'.join(words[i: i + no_rows]) for i in range(0, len(words), no_rows)]

font_size = 10
spacing_factor = 0.78
font = None
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

# bg_file = "ocean"
# bg_file = "camping"
bg_file = "bg-" + text_file
bg = Image.open(f"backgrounds/{bg_file}.jpg")
bg = bg.resize(image_size)

bg = ImageEnhance.Brightness(bg).enhance(0.7)
bg = ImageEnhance.Contrast(bg).enhance(0.7)

bg.paste(img, (0, 0), img)
bg.show()
# img.show()

# Save image
# img.save(f"posters/{words[0]}_{size}_{paper}_{resolution}.png")
bg.save(f"posters/{text_file}_{size}_{paper}_{resolution}_{bg_file}.png")
