# -*- coding: utf-8 -*-
import asyncio
import random
import re
import string

from bobotinho.apis import Dictionary
from bobotinho.bot import Bot, Message, commands, exceptions


def random_file_line(filename: str) -> str:
    with open(filename, "r", encoding="utf-8") as file:
        lines = file.read().splitlines()
    return random.choice(lines)


def is_letter(text: str) -> bool:
    return len(text) == 1 and text in string.ascii_letters


class Games(commands.Cog):

    def __init__(self, bot: Bot) -> None:
        self.bot = bot
        self.channels_playing = {}

    async def cog_check(self, ctx: commands.Context) -> bool:
        if not ctx.author.is_mod and ctx.author.name not in (ctx.channel.name, self.bot.config.dev):
            raise exceptions.ModRequired
        if ctx.channel.name in self.channels_playing:
            raise exceptions.AlreadyPlaying
        return True

    @commands.command(aliases=["hm"])
    async def hangman(self, ctx: commands.Context) -> None:
        filename = "bobotinho//data//words.txt"
        word = random_file_line(filename)
        hidden = re.sub(r"\w", "_", word)

        def check(message: Message) -> bool:
            return message.channel.name == ctx.channel.name and is_letter(message.content)

        ctx.response = f"você iniciou o jogo da forca, descubra a palavra em 2 minutos!: {hidden}"
        await self.bot.reply(ctx)
        self.channels_playing[ctx.channel.name] = {"users": [], "letters": []}

        try:
            while hidden != word:
                response = await self.bot.wait_for("message", predicate=check, timeout=120)

                ctx.channel.send(response)
        except asyncio.TimeoutError:
            ctx.response = "acabou o tempo, ninguém descobriu a palavra..."
        else:
            users: dict = {}
            for v in corrects.values():
                if v in users:
                    users[v] += 1
                else:
                    users[v] = 1
            users = sorted(users.items(), key=lambda x: x[1], reverse=True)
            users = "@" + ", @".join([f"{x[0]} ({x[1]})" for x in users])
            ctx.response = f'a palavra "{word}" foi descoberta! 🏆 {users}'
        finally:
            self.channels_playing.pop(ctx.channel.name)

        def play(message) -> bool:
            letter = message.content.lower()
            if letter in corrects or letter in wrongs:
                return False
            if letter in word:
                corrects[letter] = message.author.name
            else:
                wrongs[letter] = message.author.name
            hidden_word = "".join([x if x in corrects or x == "-" else "_" for x in word])
            if letter in word:
                ctx.bot.loop.create_task(
                    ctx.reply(f"a palavra contém a letra {letter.upper()}: {hidden_word}")
                )
            elif len(wrongs) >= 5:
                ctx.bot.loop.create_task(
                    ctx.reply(
                        f"a palavra não tem a letra {letter.upper()} e "
                        f"acabaram todas as tentativas, fim de jogo!"
                    )
                )
            else:
                ctx.bot.loop.create_task(
                    ctx.reply(
                        f"a palavra não tem a letra {letter.upper()}, "
                        f"resta(m) {5 - len(wrongs)} tentativa(s): {hidden_word}"
                    )
                )
            return hidden_word == word or len(wrongs) >= 5

    @commands.command(aliases=["lw"])
    async def longestword(self, ctx: commands.Context) -> None:
        pattern: str = "bobotinho//data//syllables.txt"
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
            if not users.values() or len(word) > len(list(users.values())[0]):
                users[message.author.name] = word
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
                "você iniciou o jogo da maior palavra, "
                f'a sílaba é "{pattern.upper()}", valendo!'
            )
            await ctx.bot.reply(ctx)
            ctx.bot.cache.set(f"game-{ctx.channel.name}", ctx.author.name, ex=30)
            waits = ctx.bot._waiting.copy()
            await ctx.bot.wait_for("message", check, timeout=30)
        except asyncio.exceptions.TimeoutError:
            if users:
                users = list(users.items())
                await ctx.send(f'fim de jogo! @{users[0][0]} venceu com a palavra "{users[0][1]}" 🏆')
            else:
                await ctx.send("fim de jogo, ninguém respondeu corretamente")
        finally:
            ctx.response = None
            ctx.bot.cache.delete(f"game-{ctx.channel.name}")
            for wait in ctx.bot._waiting:
                if wait not in waits:
                    ctx.bot._waiting.remove(wait)
                    break

    @commands.command(aliases=["mw"])
    async def mostword(self, ctx: commands.Context) -> None:
        pattern: str = "bobotinho//data//syllables.txt"
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


def prepare(bot: Bot) -> None:
    bot.add_cog(Games(bot))
