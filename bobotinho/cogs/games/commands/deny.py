# -*- coding: utf-8 -*-
description = "Recuse o desafio para lutar"


async def command(ctx):
    if name := ctx.bot.cache.get(f"fight-{ctx.author.name}"):
        ctx.response = f"você recusou o desafio contra @{name} LUL"
        ctx.bot.cache.delete(f"fight-{ctx.author.name}")
    else:
        ctx.response = "você não tem desafios para recusar"
