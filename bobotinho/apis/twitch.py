# -*- coding: utf-8 -*-
from dataclasses import dataclass

from bobotinho.apis import aiorequests
from bobotinho.exceptions import InvalidUsername


@dataclass
class Twitch:
    url: str = "http://decapi.me/twitch"
    errors: tuple = (
        "User not found",
        "be specified",
        "No user with the name",
        "There was an error",
        "Error from Twitch API",
    )

    @classmethod
    async def _request(cls, path: str, channel: str, user: str = "", *, precision: str = "3") -> str:
        url = f"{cls.url}/{path}/{channel}/{user}"
        params = {
            "lang": "pt",
            "precision": precision,
            "format": "d/m/Y \\à\\s H:i:s",
            "tz": "America/Sao_Paulo",
            "direction": "asc",
            "count": "1",
            "limit": "2",
        }
        response = await aiorequests.get(url, params=params, res_method="text")
        if any([error in response for error in cls.errors]):
            raise InvalidUsername
        elif response in (
            f"{user} does not follow {channel}",
            "A user cannot follow themself.",
            "You do not have any followers :(",
            "The list of users is empty.",
            "End of following list.",
        ):
            return None
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
        return await cls._request("uptime", channel=channel, precision=1)

    @classmethod
    async def viewers(cls, channel: str) -> str:
        return await cls._request("viewercount", channel=channel)
