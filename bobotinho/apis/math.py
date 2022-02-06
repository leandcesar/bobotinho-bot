# -*- coding: utf-8 -*-
from dataclasses import dataclass

from bobotinho.apis import aiorequests


@dataclass
class Math:
    url: str = "https://api.mathjs.org"
    version: str = "v4"

    @classmethod
    async def evaluate(cls, expression: str) -> str:
        url = f"{cls.url}/{cls.version}"
        payload = {"expr": expression, "precision": "4"}
        response = await aiorequests.post(url, json=payload)
        return response.get("result") or response.get("error")
