# -*- coding: utf-8 -*-
from aiohttp import ClientSession


class Webhook:
    session: ClientSession = ClientSession()

    async def discord(self, url: str, *, content: str, user_name: str = None, user_avatar_url: str = None) -> bool:
        data = {"username": user_name, "content": content}
        if user_avatar_url:
            data["avatar_url"] = user_avatar_url
        async with self.session.request("post", url, json=data) as response:
            return response.ok
