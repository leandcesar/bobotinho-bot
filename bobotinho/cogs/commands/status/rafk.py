# -*- coding: utf-8 -*-
from bobotinho.cogs.commands.status import afks
from bobotinho.database import models

description = "Retome seu status de ausência do chat"
aliases = [f"r{alias}" for alias in list(afks.keys())[1:]]
usage = "digite o comando em até 3 minutos após ter retornado do seu AFK para retomá-lo"


async def func(ctx):
    if afk := ctx.bot.cache.get(f"afk-{ctx.author.id}"):
        ctx.bot.cache.delete(f"afk-{ctx.author.id}")
        afk_type = afks[ctx.command.invocation[1:]]
        content = afk.get("content")
        await models.Afk.create(
            user_id=ctx.author.id,
            alias=ctx.command.invocation[1:],
            content=content,
            created_at=afk.get("created_at"),
        )
        ctx.response = f"você continuou {afk_type.rafk}: {content or afk_type.emoji}"
