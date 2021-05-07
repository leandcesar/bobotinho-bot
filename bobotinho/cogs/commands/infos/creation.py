# -*- coding: utf-8 -*-
from bobotinho.apis import twitch
from bobotinho.utils import checks, convert

description = "Saiba quando algum usuário criou sua conta"
aliases = ["create"]
usage = "digite o comando e o nome de alguém para saber a data de criação da conta"
extra_checks = [checks.is_banword]


async def func(ctx, arg: str = None):
    name = convert.str2username(arg) or ctx.author.name
    if not name:
        ctx.response = "nome de usuário inválido"
    elif name == ctx.bot.nick:
        ctx.response = "eu sempre existi..."
    else:
        creation = await twitch.TwitchAPI.creation(name)
        mention = "você" if name == ctx.author.name else f"@{name}"
        if not creation:
            ctx.response = "não foi possível verificar isso"
        elif "não existe" in creation:
            ctx.response = creation
        else:
            ctx.response = f"{mention} criou a conta em {creation}"