# -*- coding: utf-8 -*-
from bobotinho.cogs.tools import afks
from bobotinho.database import Afk

description = "Informe que você está se ausentando do chat"
aliases = list(afks.keys())[1:]
extra_checks = ["Check.allowed", "Check.banword"]


async def command(ctx, *, content: str = ""):
    if content and len(content) > 400:
        ctx.response = "essa mensagem é muito comprida"
    else:
        invoke_by = ctx.message.content.partition(" ")[0][len(ctx.prefix):].lower()
        afk_type = afks[invoke_by]
        await Afk.create(
            user_id=ctx.author.id,
            alias=invoke_by,
            content=content,
        )
        ctx.response = f"você {afk_type.afk}: {content or afk_type.emoji}"
