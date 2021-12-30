# -*- coding: utf-8 -*-
from dataclasses import dataclass

from bobotinho.apis import aiorequests

__all__ = "Analytics"


@dataclass
class Analytics:
    """Bot metrics analytics."""

    key: str
    url: str = "https://tracker.dashbot.io/track"
    version: str = "11.1.0-rest"
    platform: str = "universal"

    def params(self, type: str) -> dict:
        """Build query params for HTTP request."""
        return {"type": type, "v": self.version, "platform": self.platform, "apiKey": self.key}

    def json(self, *, text: str, id: str, name: str, locale: str, extra_json: dict = {}) -> dict:
        """Build JSON payload for HTTP request."""
        user_json = {"firstName": name, "locale": locale}
        return {"userId": id, "text": text, "platformJson": extra_json, "platformUserJson": user_json}

    async def received(self, author_id: int, author_name: str, channel_name: int, message: str) -> None:
        """When the bot receives a message."""
        params = self.params(type="incoming")
        json = self.json(text=message, id=author_id, name=author_name, locale=channel_name)
        await aiorequests.post(self.url, params=params, json=json, raise_for_status=False, wait_response=False)

    async def sent(self, author_id: int, author_name: str, channel_name: int, message: str) -> None:
        """When the bot sends a message."""
        params = self.params(type="outgoing")
        json = self.json(text=message, id=author_id, name=author_name, locale=channel_name)
        await aiorequests.post(self.url, params=params, json=json, raise_for_status=False, wait_response=False)
