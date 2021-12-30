# -*- coding: utf-8 -*-
from dataclasses import dataclass

from bobotinho.apis import aiorequests

__all__ = "Color"


@dataclass
class Color:
    """Color API."""

    url: str = "https://www.thecolorapi.com"

    @classmethod
    async def name(cls, hex_color: str) -> str:
        """Get color name from HEX color code."""
        url = f"{cls.url}/id"
        params = {"hex": hex_color}
        response = await aiorequests.get(url, params=params)
        return response["name"]["value"]
