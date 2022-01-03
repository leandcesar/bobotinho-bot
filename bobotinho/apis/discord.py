# -*- coding: utf-8 -*-
from dataclasses import dataclass

from bobotinho.apis import aiorequests

__all__ = "Discord"


@dataclass
class Discord:

    @staticmethod
    async def webhook(url: str, data: dict) -> None:
        data = {
            "embeds": [
                {
                    "title": data.get("title"),
                    "url": data.get("link"),
                    "description": data.get("description"),
                    "color": data.get("color"),
                    "thumbnail": {"url": data.get("thumbnail")},
                    "image": {"url": data.get("image")},
                    "author": {
                        "name": data.get("author"),
                        "icon_url": data.get("author_icon"),
                        "url": data.get("author_link"),
                    },
                    "footer": {
                        "text": data.get("footer"),
                        "icon_url": data.get("footer_icon"),
                    },
                    "timestamp": (
                        data["timestamp"].strftime("%Y-%m-%dT%H:%M:%SZ")
                        if data.get("timestamp")
                        else None
                    ),
                }
            ]
        }
        await aiorequests.post(url, json=data, wait_response=False)
