# -*- coding: utf-8 -*-
description = "Receba o link da lista de comandos ou veja como utilizar um comando específico"
aliases = ["commands"]


async def command(ctx, arg: str = ""):
    c = None
    for command in ctx.bot.commands.values():
        if arg == command.name or (command.aliases and arg in command.aliases):
            c = command
            break
    if not c:
        ctx.response = f"veja todos os comandos: {ctx.bot.config.site_url}/docs/help"
    elif c.aliases:
        aliases = ", ".join([ctx.prefix + alias for alias in c.aliases])
        ctx.response = f"{ctx.prefix}{c.name} ({aliases}): {c.description}"
    else:
        ctx.response = f"{ctx.prefix}{c.name}: {c.description}"
