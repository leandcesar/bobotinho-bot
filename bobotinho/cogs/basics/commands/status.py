# -*- coding: utf-8 -*-
description = "Receba o link para ver o status dos softwares do bot"


async def command(ctx):
    ctx.response = f"veja os status dos softwares: {ctx.bot.config.site_url}/status"
