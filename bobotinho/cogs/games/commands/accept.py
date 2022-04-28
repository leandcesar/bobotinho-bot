# -*- coding: utf-8 -*-
import random

description = "Aceite o desafio para lutar"


async def command(ctx):
    if name := ctx.bot.cache.get(f"fight-{ctx.author.name}"):
        fighters = ["você", "@" + name]
        random.shuffle(fighters)
        quote = random.choice(
            [
                f"{fighters[0]} acaba com {fighters[1]}",
                f"{fighters[0]} deixa {fighters[1]} desacordado",
                f"{fighters[0]} derrota {fighters[1]} facilmente",
                f"{fighters[0]} espanca {fighters[1]} sem piedade",
                f"{fighters[0]} não dá chances para {fighters[1]} e vence",
                f"{fighters[0]} quase perde, mas derruba {fighters[1]}",
                f"{fighters[0]} vence a luta contra {fighters[1]}",
                f"{fighters[0]} vence {fighters[1]} com dificuldades",
                f"{fighters[0]} vence {fighters[1]} em uma luta acirrada",
                f"{fighters[0]} vence {fighters[1]} facilmente",
            ]
        )
        ctx.response = f"{quote}! GG"
        ctx.bot.cache.delete(f"fight-{ctx.author.name}")
    else:
        ctx.response = "você não tem desafios para aceitar"
