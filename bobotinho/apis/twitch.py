# -*- coding: utf-8 -*-
from dataclasses import dataclass

from bobotinho.apis import aiorequests

__all__ = "Twitch"

ERRORS = ("error", "not follow", "be specified", "no user", "not found", "cannot follow", "not have")


@dataclass
class Twitch:
    """Twitch user and channel informations API."""

    url: str = "http://decapi.me/twitch"

    @classmethod
    async def _request(cls, path: str) -> str:
        url = f"{cls.url}/{path}"
        params = {
            "lang": "pt",
            "precision": "3",
            "format": "d/m/Y \\à\\s H:i:s",
            "tz": "America/Sao_Paulo",
            "direction": "asc",
            "count": "1",
            "limit": "2",
        }
        response = await aiorequests.get(url, params=params, res_method="text")
        if response.startswith("No user with the name"):
            user = response.split('"')[1]
            return f"@{user} não existe"
        if any(error in response.lower() for error in ERRORS):
            return ""
        if path.startswith(("following", "followers", "random_user")):
            return response.split(", ")[0]
        return response

    @classmethod
    async def age(cls, user: str) -> str:
        """Account age of the specified user."""
        return await cls._request(f"accountage/{user}")

    @classmethod
    async def avatar(cls, user: str) -> str:
        """Avatar URL for the specified user."""
        return await cls._request(f"avatar/{user}")

    @classmethod
    async def creation(cls, user: str) -> str:
        """Creation datetime of the specified user."""
        return await cls._request(f"creation/{user}")

    @classmethod
    async def follow_age(cls, channel: str, user: str) -> str:
        """Time difference between when user followed channel."""
        return await cls._request(f"followage/{channel}/{user}")

    @classmethod
    async def follows(cls, channel: str) -> str:
        """Current amount of followers a Twitch channel has."""
        return await cls._request(f"followcount/{channel}")

    @classmethod
    async def followed(cls, channel: str, user: str) -> str:
        """Datetime of when the user followed the channel."""
        return await cls._request(f"followed/{channel}/{user}")

    @classmethod
    async def follower(cls, channel: str) -> str:
        """Followers a channel has."""
        return await cls._request(f"followers/{channel}")

    @classmethod
    async def following(cls, user: str) -> str:
        """Channels that the specified user is following."""
        return await cls._request(f"following/{user}")

    @classmethod
    async def game(cls, channel: str) -> str:
        """Current game the channel has been set to."""
        return await cls._request(f"game/{channel}")

    @classmethod
    async def random_user(cls, channel: str) -> str:
        """Random user that are currently logged into chat in the specified channel."""
        return await cls._request(f"random_user/{channel}")

    @classmethod
    async def title(cls, channel: str) -> str:
        """Current title set on the channel."""
        return await cls._request(f"title/{channel}")

    @classmethod
    async def views(cls, channel: str) -> str:
        """Total views a channel has."""
        return await cls._request(f"total_views/{channel}")

    @classmethod
    async def uptime(cls, channel: str) -> str:
        """How long the specified channel has been live for the current stream."""
        return await cls._request(f"uptime/{channel}")

    @classmethod
    async def viewers(cls, channel: str) -> str:
        """Total viewers the channel has, if they are currently streaming."""
        return await cls._request(f"viewercount/{channel}")
