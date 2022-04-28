# -*- coding: utf-8 -*-
description = "Cancele o desafio para lutar"


async def command(ctx):
    for key in ctx.bot.cache.keys(pattern="fight"):
        if ctx.author.name == ctx.bot.cache.get(key):
            name = key.split("-")[1]
            ctx.response = f"você cancelou o desafio contra @{name}"
            ctx.bot.cache.delete(key)
            break
    else:
        ctx.response = "você não tem desafios para cancelar"
