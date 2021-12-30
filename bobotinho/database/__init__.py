# -*- coding: utf-8 -*-
from tortoise import Tortoise


async def init(self, db_url: str):
    models = ["bobotinho.database.models"]
    await Tortoise.init(db_url=db_url, modules={"models": models})
    await Tortoise.generate_schemas(safe=True)


async def close(self):
    await Tortoise.close_connections()
