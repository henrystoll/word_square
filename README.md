# Word Square

## Installation

```
python3 -m pip install --upgrade pip
python3 -m pip install --upgrade Pillow
```

## Generate Word Square
Generates the grid
 - Comment out `random.seed()` to get random results for each run.
 - `size` of the square grid
 - `paper` e.g. DIN A3
 - `resolution` in dpi, either 300 (print) or 72 (web)
 - `words` not sorted list of the words that will be set in the grid
 - `header` input header text for variants 
 - `sub_header` input subheader text for variants
 - `variant` select the variant for a header and subheader 
 - `bg_color` color of background, use triple for RGB values
 - `text_color` color of text
 - `no_columns` number of columns for the word list
 - `no_rows` number of rows for the word list
```
python3 word_square.py
```
 