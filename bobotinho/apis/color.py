# -*- coding: utf-8 -*-
from dataclasses import dataclass

from bobotinho.apis import aiorequests


@dataclass
class Color:
    url: str = "https://www.thecolorapi.com"

    @classmethod
    async def name(cls, hex_color: str) -> str:
        url = f"{cls.url}/id"
        params = {"hex": hex_color[1:] if hex_color[0] == "#" else hex_color}
        response = await aiorequests.get(url, params=params)
        return response["name"]["value"]
