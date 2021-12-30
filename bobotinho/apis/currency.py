# -*- coding: utf-8 -*-
from dataclasses import dataclass

from bobotinho.apis import aiorequests

__all__ = "Currency"


@dataclass
class Currency:
    """Currency converter API."""

    key: str
    url: str = "https://rest.coinapi.io"
    version: str = "v1"

    async def convert(self, base: str, to: str) -> float:
        """Get exchange rate between pair of requested assets."""
        url = f"{self.url}/{self.version}/exchangerate/{base.upper()}/{to.upper()}"
        headers = {"Accept": "application/json", "X-CoinAPI-Key": self.key}
        response = await aiorequests.get(url, headers=headers)
        return response["rate"]

    async def rates(self, base: str) -> dict:
        """Get the current exchange rate between requested asset and all other assets."""
        url = f"{self.url}/{self.version}/exchangerate/{base.upper()}"
        headers = {"Accept": "application/json", "X-CoinAPI-Key": self.key}
        response = await aiorequests.get(url, headers=headers)
        return {rate["asset_id_quote"]: rate["rate"] for rate in response["rates"]}
