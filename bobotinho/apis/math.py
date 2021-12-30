# -*- coding: utf-8 -*-
from dataclasses import dataclass

from bobotinho.apis import aiorequests

__all__ = "Math"


@dataclass
class Math:
    """Math API."""

    url: str = "https://api.mathjs.org"
    version: str = "v4"

    @classmethod
    async def evaluate(cls, expression: str) -> str:
        """Evaluate the expression."""
        url = f"{cls.url}/{cls.version}"
        params = {"expr": expression, "precision": "4"}
        response = await aiorequests.post(url, params=params)
        return response.get("result") or response.get("error")
