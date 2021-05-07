# -*- coding: utf-8 -*-
from bobotinho.database import models
from bobotinho.utils import checks

description = "Despause o bot"
extra_checks = [checks.is_mod]
no_global_checks = True


async def func(ctx):
    if ctx.bot.channels[ctx.channel.name]["status"]:
        ctx.response = "já estou ligado ☕"
    else:
        ctx.bot.channels[ctx.channel.name]["status"] = True
        await models.Channel.filter(user_id=ctx.channel.name).update(status=True)
        ctx.response = "você me ligou ☕"