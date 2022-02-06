# -*- coding: utf-8 -*-
import random
import re

from bobotinho.bot import Bot, Context, command, commands


def to_username(name: str) -> str:
    return name.lstrip("@").rstrip(",").lower() if name else ""


class Interactive(commands.Cog):

    def __init__(self, bot: Bot) -> None:
        self.bot = bot

    @command()
    async def accept(self, ctx: Context) -> None:
        name = self.bot.cache.get(f"fight-{ctx.author.name}")
        if name:
            self.bot.cache.delete(f"fight-{ctx.author.name}")
            fighters = ["você", f"@{name}"]
            random.shuffle(fighters)
            quote = random.choice(
                [
                    f"{fighters[0]} acaba com {fighters[1]}",
                    f"{fighters[0]} deixa {fighters[1]} desacordado",
                    f"{fighters[0]} derrota {fighters[1]} facilmente",
                    f"{fighters[0]} espanca {fighters[1]} sem piedade",
                    f"{fighters[0]} vence sem dar chances para {fighters[1]}",
                    f"{fighters[0]} quase perde, mas derruba {fighters[1]}",
                    f"{fighters[0]} vence a luta contra {fighters[1]}",
                    f"{fighters[0]} vence {fighters[1]} com dificuldades",
                    f"{fighters[0]} vence {fighters[1]} em uma luta acirrada",
                    f"{fighters[0]} vence {fighters[1]} facilmente",
                ]
            )
            ctx.response = f"{quote}!"
        else:
            ctx.response = "você não tem desafios para aceitar"

    @command()
    async def cancel(self, ctx: Context) -> None:
        for key in self.bot.cache.keys(pattern="fight"):
            if ctx.author.name == self.bot.cache.get(key):
                self.bot.cache.delete(key)
                name = key.split("-")[1]
                ctx.response = f"você cancelou o desafio contra @{name}"
                break
        else:
            ctx.response = "você não tem desafios para cancelar"

    @command()
    async def deny(self, ctx: Context) -> None:
        name = ctx.bot.cache.get(f"fight-{ctx.author.name}")
        if name:
            ctx.response = f"você recusou o desafio contra @{name}"
            ctx.bot.cache.delete(f"fight-{ctx.author.name}")
        else:
            ctx.response = "você não tem desafios para recusar"

    @command(usage="digite o comando e um usuário que deseja desafiar para luta")
    async def fight(self, ctx: Context, name: str) -> None:
        name = to_username(name)
        if name == self.bot.nick:
            ctx.response = "você não conseguiria me derrotar..."
        elif name == ctx.author.name:
            ctx.response = "você iniciou uma luta interna..."
        elif someone := self.bot.cache.get(f"fight-{ctx.author.name}"):
            ctx.response = (
                f"você já está sendo desafiado por @{someone}, "
                f'digite "{self.bot.prefix}accept" ou "{self.bot.prefix}deny"'
            )
        elif someone := self.bot.cache.get(f"fight-{name}"):
            ctx.response = f"@{name} já está sendo desafiado por @{someone}"
        else:
            self.bot.cache.set(f"fight-{name}", ctx.author.name, ex=120)
            ctx.response = (
                f"você desafiou @{name}, aguarde o usuário "
                f'digitar "{self.bot.prefix}accept" ou "{self.bot.prefix}deny"'
            )

    @commands.cooldown(rate=2, per=15)
    @command(usage="digite o comando e um usuário que deseja abraçar")
    async def hug(self, ctx: Context, name: str) -> None:
        name = to_username(name)
        ctx.response = (
            "🤗"
            if name == self.bot.nick
            else "você tentou se abraçar..."
            if name == ctx.author.name
            else f"você abraçou @{name} 🤗"
        )

    @commands.cooldown(rate=2, per=15)
    @command(usage="digite o comando e um usuário que deseja beijar")
    async def kiss(self, ctx: Context, name: str) -> None:
        name = to_username(name)
        ctx.response = (
            "😳"
            if name == self.bot.nick
            else "você tentou se beijar..."
            if name == ctx.author.name
            else f"você deu um beijinho em @{name} 😚"
        )

    @commands.cooldown(rate=2, per=15)
    @command(usage="digite o comando e um usuário para ver quanto há de amor")
    async def love(self, ctx: Context, *, content: str) -> None:
        emojis = ["😭", "😥", "💔", "😢", "😐", "😊", "❤", "💕", "💘", "😍", "PogChamp ❤"]
        match = re.match(r"([\w\s]+)\s&\s([\w\s]+)+$", content)  # Foo & bar
        if match:
            seed_1 = sum([ord(char) for char in match.group(1)])
            seed_2 = sum([ord(char) for char in match.group(2)])
        else:
            seed_1 = sum([ord(char) for char in ctx.author.name])
            seed_2 = sum([ord(char) for char in to_username(content)])
        percentage = (seed_1 + seed_2) % 101
        emoji = emojis[round(percentage / 10)]
        if match:
            ctx.response = f"entre {content}: {percentage}% de amor {emoji}"
        else:
            ctx.response = f"você & {content}: {percentage}% de amor {emoji}"

    @commands.cooldown(rate=2, per=15)
    @command(usage="digite o comando e um usuário que deseja fazer cafuné")
    async def pat(self, ctx: Context, name: str) -> None:
        name = to_username(name)
        ctx.response = (
            "😊"
            if name == self.bot.nick
            else "você tentou fazer cafuné em si mesmo... FeelsBadMan"
            if name == ctx.author.name
            else f"você fez cafuné em @{name} 😊"
        )

    @commands.cooldown(rate=2, per=15)
    @command(usage="digite o comando e dois usuários para shipá-los")
    async def ship(self, ctx: Context, name_1: str, name_2: str = "") -> None:
        name_1 = to_username(name_1)
        name_2 = to_username(name_2)
        if not name_2:
            name_1, name_2 = ctx.author.name, name_1
        if name_1 == name_2:
            ctx.response = "uma pessoa não pode ser shipada com ela mesma..."
        else:
            ship_1 = name_1[:len(name_1) // 2 + 1]
            ship_2 = name_2[len(name_2) // 2:]
            if name_1 == ctx.author.name:
                ctx.response = f"você & {name_2}: {ship_1 + ship_2} 😍"
            else:
                ctx.response = f"{name_1} & {name_2}: {ship_1 + ship_2} 😍"

    @commands.cooldown(rate=2, per=15)
    @command(usage="digite o comando e um usuário que deseja dar um tapa")
    async def slap(self, ctx: Context, name: str) -> None:
        name = to_username(name)
        ctx.response = (
            "vai bater na mãe 😠"
            if name == self.bot.nick
            else "você se deu um tapa..."
            if name == ctx.author.name
            else f"você deu um tapinha em @{name} 👋"
        )

    @commands.cooldown(rate=2, per=15)
    @command(usage="digite o comando e um usuário que deseja colocar pra dormir")
    async def tuck(self, ctx: Context, name: str) -> None:
        name = to_username(name)
        ctx.response = (
            "eu não posso dormir agora..."
            if name == self.bot.nick
            else "você foi para a cama"
            if name == ctx.author.name
            else f"você colocou @{name} na cama 🙂👉🛏"
        )


def prepare(bot: Bot) -> None:
    bot.add_cog(Interactive(bot))
