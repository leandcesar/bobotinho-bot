# -*- coding: utf-8 -*-
import html
from dataclasses import dataclass

from bobotinho.apis import aiorequests

__all__ = "Dictionary"


@dataclass
class Dictionary:
    """Portuguese (Brazilian) dictionary API."""

    url: str = "http://www.dicio.com.br"

    @classmethod
    async def search(cls, word: str) -> str:
        """Search for a word to check if it exists."""
        url = f"{cls.url}/{word}"
        response = await aiorequests.get(url, res_method="text")
        try:
            text = html.unescape(response)
            start = text.find("<h1")
            if start != -1:
                start += len("<h1")
            start = text.find(">", start) + 1
            end = text.find("</h1>", start)
            return text[start:end] if -1 < start < end else text
        except Exception:
            return ""
