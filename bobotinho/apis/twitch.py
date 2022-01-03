# -*- coding: utf-8 -*-
from dataclasses import dataclass

from bobotinho.apis import aiorequests
from bobotinho.exceptions import InvalidUsername, HTTPException

__all__ = "Twitch"


@dataclass
class Twitch:
    url: str = "http://decapi.me/twitch"

    @classmethod
    async def _request(cls, path: str, channel: str, user: str = "") -> str:
        url = f"{cls.url}/{path}/{channel}/{user}"
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
        if response in (
            f"User not found: {channel}",
            f"User not found: {user}",
            "A username has to be specified.",
            "A channel name has to be specified.",
            "Both username and channel name must be specified.",
            f"No user with the name \"{channel}\" found.",
            f"No user with the name \"{user}\" found.",
            f"There was an error retrieving users for channel: {channel}",
        ):
            raise InvalidUsername
        elif response in (
            f"{user} does not follow {channel}",
            "A user cannot follow themself.",
            "You do not have any followers :(",
            "The list of users is empty.",
            "End of following list.",
        ):
            return None
        elif response.startswith("[Error from Twitch API]"):
            raise HTTPException
        if path.startswith(("following", "followers", "random_user")):
            return response.split(", ")[0]
        return response

    @classmethod
    async def age(cls, user: str = "cellbit") -> str:
        return await cls._request("accountage", channel=user)

    @classmethod
    async def avatar(cls, user: str = "cellbit") -> str:
        return await cls._request("avatar", channel=user)

    @classmethod
    async def creation(cls, user: str = "cellbit") -> str:
        return await cls._request("creation", channel=user)

    @classmethod
    async def follow_age(cls, channel: str, user: str = "cellbit") -> str:
        return await cls._request("followage", channel=channel, user=user)

    @classmethod
    async def follows(cls, channel: str) -> str:
        return await cls._request("followcount", channel=channel)

    @classmethod
    async def followed(cls, channel: str, user: str = "cellbit") -> str:
        return await cls._request("followed", channel=channel, user=user)

    @classmethod
    async def follower(cls, channel: str) -> str:
        return await cls._request("followers", channel=channel)

    @classmethod
    async def following(cls, user: str = "cellbit") -> str:
        return await cls._request("following", channel=user)

    @classmethod
    async def game(cls, channel: str) -> str:
        return await cls._request("game", channel=channel)

    @classmethod
    async def random_user(cls, channel: str) -> str:
        return await cls._request("random_user", channel=channel)

    @classmethod
    async def title(cls, channel: str) -> str:
        return await cls._request("title", channel=channel)

    @classmethod
    async def views(cls, channel: str) -> str:
        return await cls._request("total_views", channel=channel)

    @classmethod
    async def uptime(cls, channel: str) -> str:
        return await cls._request("uptime", channel=channel)

    @classmethod
    async def viewers(cls, channel: str) -> str:
        return await cls._request("viewercount", channel=channel)
