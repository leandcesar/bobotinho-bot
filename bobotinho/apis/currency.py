# -*- coding: utf-8 -*-
from dataclasses import dataclass

from bobotinho.apis import aiorequests

__all__ = "Currency"


@dataclass
class Currency:
    key: str
    url: str = "https://rest.coinapi.io"
    version: str = "v1"

    async def convert(self, base: str, to: str) -> float:
        url = f"{self.url}/{self.version}/exchangerate/{base.upper()}/{to.upper()}"
        headers = {"Accept": "application/json", "X-CoinAPI-Key": self.key}
        response = await aiorequests.get(url, headers=headers)
        return response["rate"]
