# -*- coding: utf-8 -*-
from bobotinho.apis import Twitch
from bobotinho.utils import convert, timetools

description = "Saiba há quanto tempo algum usuário criou sua conta"
aliases = ["age"]
usage = "digite o comando e o nome de alguém para saber a data de criação da conta"


async def command(ctx, arg: str = ""):
    name = convert.str2name(arg, default=ctx.author.name)
    if name == ctx.bot.nick:
        ctx.response = "eu sempre existi..."
    else:
        accountage = await Twitch.age(name)
        mention = "você" if name == ctx.author.name else f"@{name}"
        if not accountage:
            ctx.response = "não foi possível verificar isso"
        elif "não existe" in accountage:
            ctx.response = accountage
        elif age := timetools.birthday(accountage):
            ctx.response = f"hoje completa {age} que {mention} criou a conta 🎂"
        else:
            ctx.response = f"{mention} criou a conta há {accountage}"
