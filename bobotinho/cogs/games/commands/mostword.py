# -*- coding: utf-8 -*-
import asyncio

from bobotinho.apis import Dictionary
from bobotinho.utils import convert

aliases = ["mw"]
description = "Jogo de mais palavras com determinada sílaba, dura 30 segundas"
extra_checks = ["Role.admin", "Check.game"]


async def command(ctx):
    pattern: str = convert.txt2randomline("bobotinho//data//syllables.txt")
    users: dict = {}
    words: list = []

    def play(message) -> bool:
        if len(message.content.split(" ")) != 1:
            return False
        if not message.content.isalpha():
            return False
        word = message.content.lower()
        if pattern not in word or word in words:
            return False
        words.append(word)
        search = asyncio.run(Dictionary.search(word))
        if not convert.str2ascii(search) == convert.str2ascii(word):
            return False
        if users.get(message.author.name):
            users[message.author.name] += 1
        else:
            users[message.author.name] = 1
        return False

    def check(message) -> bool:
        if message.echo:
            return False
        if message.channel.name != ctx.channel.name:
            return False
        if not ctx.bot.channels[message.channel.name]["online"]:
            return False
        return play(message)

    try:
        ctx.response = (
            "você iniciou o jogo de mais palavras, "
            f'a sílaba é "{pattern.upper()}", valendo!'
        )
        await ctx.bot.reply(ctx)
        ctx.bot.cache.set(f"game-{ctx.channel.name}", ctx.author.name, ex=30)
        waits = ctx.bot._waiting.copy()
        await ctx.bot.wait_for("message", check, timeout=30)
    except asyncio.exceptions.TimeoutError:
        if users:
            users = sorted(users.items(), key=lambda x: x[1], reverse=True)
            await ctx.send(f"fim de jogo! @{users[0][0]} venceu com {users[0][1]} palavras 🏆")
        else:
            await ctx.send("fim de jogo, ninguém respondeu corretamente")
    finally:
        ctx.response = None
        ctx.bot.cache.delete(f"game-{ctx.channel.name}")
        for wait in ctx.bot._waiting:
            if wait not in waits:
                ctx.bot._waiting.remove(wait)
                break
