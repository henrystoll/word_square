from io import BytesIO
from os import walk
from typing import Optional

import fastapi
import uvicorn
from pydantic import BaseModel
from starlette.responses import StreamingResponse

from word_square import generate_poster


class Poster(BaseModel):
    words: list[str] = [
        "adventure",
        "backpack",
        "bonfire",
        "canteen",
        "compass",
        "grizzly",
        "hammock",
        "hike",
        "kindling",
        "lantern",
        "rucksack",
        "smore",
        "stake",
        "sunblock",
        "tent",
        "trail",
        "camper",
        "provisions",
        "bushman",
        "stove"
    ]
    background: Optional[str] = None
    grid_size: Optional[int] = 20
    no_columns: Optional[int] = 4
    paper: Optional[str] = 'DIN_A3'
    resolution: Optional[str] = 300
    margin_height_percent: Optional[int] = 10
    variant: Optional[str] = 'en-1'
    bg_color_str: Optional[str] = "#000"
    text_color_str: Optional[str] = "custom(DARK_WHITE)"


api = fastapi.FastAPI()


@api.get('/backgrounds')
def list_backgrounds():
    path = './backgrounds'
    _, _, filenames = next(walk(path))
    filenames = [file.split('.')[0] for file in filenames if file.endswith('.jpg')]
    return filenames


@api.post('/image')
async def generate_image(settings: Poster):
    img = generate_poster(settings.words)
    buffer = BytesIO()
    img.save(buffer, format='PNG')
    buffer.seek(0)
    return StreamingResponse(buffer, media_type="image/png",
                             # headers={'Content-Disposition': 'inline; filename=image.png"'}
                             )


uvicorn.run(api)
