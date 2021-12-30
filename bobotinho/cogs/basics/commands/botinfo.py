# -*- coding: utf-8 -*-
description = "Veja as principais informações sobre o bot"
aliases = ["bot", "info"]


async def command(ctx):
    ctx.response = (
        f"estou conectado à {len(ctx.bot.channels)} canais, "
        f"com {len(ctx.bot.commands)} comandos, "
        f"feito por @{ctx.bot.config.dev} em Python e hospedado em Heroku"
    )
