# -*- coding: utf-8 -*-
import html
from dataclasses import dataclass

from bobotinho.apis import aiorequests


@dataclass
class Dictionary:
    url: str = "http://www.dicio.com.br"

    @classmethod
    async def exists(cls, word: str) -> bool:
        url = f"{cls.url}/{word}"
        response = await aiorequests.get(url, res_method="text")
        text = html.unescape(response)
        start = text.find("<h1")
        if start != -1:
            start += len("<h1")
        start = text.find(">", start) + 1
        end = text.find("</h1>", start)
        find = text[start:end] if -1 < start < end else text
        return find.lower() == text.lower()
