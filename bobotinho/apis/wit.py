# -*- coding: utf-8 -*-
from dataclasses import dataclass

from bobotinho.apis import aiorequests

__all__ = "Wit"


@dataclass
class Wit:
    token: str
    url: str = "https://api.wit.ai"
    version: str = "20200513"

    @classmethod
    async def detect(cls, text: str) -> str:
        url = f"{cls.url}/message"
        params = {"q": text}
        headers = {
            "authorization": f"Bearer {cls.token}",
            "accept": f"application/vnd.wit.{cls.version}+json"
        }
        response = await aiorequests.get(url, headers=headers, params=params)
        try:
            return response["entities"]["wit$datetime:datetime"][0]
        except KeyError:
            return ""
