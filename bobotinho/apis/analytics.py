# -*- coding: utf-8 -*-
from dataclasses import dataclass

from bobotinho.apis import aiorequests


@dataclass
class Analytics:
    key: str
    url: str = "https://tracker.dashbot.io/track"
    version: str = "11.1.0-rest"
    platform: str = "universal"

    def _params(self, type: str) -> dict:
        return {"type": type, "v": self.version, "platform": self.platform, "apiKey": self.key}

    def _payload(self, *, text: str, id: str, name: str, locale: str, extra_json: dict = {}) -> dict:
        user_json = {"firstName": name, "locale": locale}
        return {"userId": id, "text": text, "platformJson": extra_json, "platformUserJson": user_json}

    async def received(self, author_id: int, author_name: str, channel_name: int, message: str) -> None:
        params = self._params(type="incoming")
        payload = self._payload(text=message, id=author_id, name=author_name, locale=channel_name)
        await aiorequests.post(self.url, params=params, json=payload, raise_for_status=False, wait_response=False)

    async def sent(self, author_id: int, author_name: str, channel_name: int, message: str) -> None:
        params = self._params(type="outgoing")
        payload = self._payload(text=message, id=author_id, name=author_name, locale=channel_name)
        await aiorequests.post(self.url, params=params, json=payload, raise_for_status=False, wait_response=False)
