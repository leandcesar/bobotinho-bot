# -*- coding: utf-8 -*-
from bobotinho import config
from bobotinho.api import Api
from bobotinho.commands import Bot, Checks, Cog, Context, check, command, cooldown, helper
from bobotinho.exceptions import InvalidName


def username(name: str) -> str:
    return name.lstrip("@").rstrip(",").lower()


class FunCog(Cog):

    def __init__(self, bot: Bot, *, api: Api):
        self.bot = bot
        self.api = api

    @command()
    @cooldown(rate=1, per=10)
    @helper(description="Dê um abraço em alguém do chat", usage="digite o comando e o nome de alguém para abracá-lo")
    async def hug(self, ctx: Context, name: str) -> None:
        name = username(name)
        if name == self.bot.nick:
            ctx.response = "🤗"
        elif name == ctx.author.name:
            ctx.response = "você tentou se abraçar... FeelsBadMan"
        else:
            ctx.response = f"você abraçou @{name} 🤗"

    @command(aliases=["4head", "hahaa"])
    @cooldown(rate=1, per=10)
    @helper(description="Receba uma piada ou trocadilho")
    async def joke(self, ctx: Context) -> None:
        joke = await self.api.joke()
        if joke:
            ctx.response = f"{joke} 4Head"

    @command()
    @cooldown(rate=1, per=10)
    @helper(description="Dê um beijinho em alguém do chat", usage="digite o comando e o nome de alguém para beijá-lo")
    async def kiss(self, ctx: Context, name: str) -> None:
        name = username(name)
        if name == self.bot.nick:
            ctx.response = "😳"
        elif name == ctx.author.name:
            ctx.response = "você tentou se beijar... FeelsBadMan"
        else:
            ctx.response = f"você deu um beijinho em @{name} 😚"

    @command(aliases=["ship"])
    @cooldown(rate=1, per=10)
    @helper(description="Veja quanto de amor existe entre o ship de duas pessoas", usage="digite o comando e o nome de uma ou duas pessoas")
    async def love(self, ctx: Context, name1: str, name2: str = None) -> None:
        name1 = username(name1)
        if name2 is None:
            name1, name2 = ctx.author.name, name1
        else:
            name2 = username(name2)
        if name1 == name2:
            ctx.response = "uma pessoa não pode ser shipada com ela mesma..."
        else:
            ship1 = name1[:len(name1)//2 + 1] if len(name1) > 2 else name1
            ship2 = name2[len(name2)//2:] if len(name2) > 2 else name2
            ship = ship1 + ship2
            emojis = ["😭", "😥", "💔", "😢", "😐", "😊", "❤", "💕", "💘", "😍", "PogChamp ❤"]
            percentage = int("".join(x for x in ship if x in "abcdefghijklmnopqrstuvxywz0123456789").encode().hex()) % 101
            emoji = emojis[round(percentage / 10)]
            ctx.response = f"{name1} & {name2}: {ship} com {percentage}% de amor {emoji}"

    @command()
    @cooldown(rate=1, per=10)
    @helper(description="Faça carinho em alguém do chat", usage="digite o comando e o nome de alguém para fazer carinho")
    async def pat(self, ctx: Context, name: str) -> None:
        name = username(name)
        if name == self.bot.nick:
            ctx.response = "😊"
        elif name == ctx.author.name:
            ctx.response = "você tentou fazer cafuné em si mesmo... FeelsBadMan"
        else:
            ctx.response = f"você fez cafuné em @{name} 😊"

    @command()
    @cooldown(rate=1, per=10)
    @helper(description="É... é isso mesmo")
    async def penis(self, ctx: Context, name: str = None) -> None:
        name = ctx.author.name if name is None else username(name)
        if name == self.bot.nick:
            ctx.response = "eu sou um robô..."
        else:
            length = int(name.encode().hex()) % 24 + 6
            emoji = "🤏" if length <= 13 else "🍌" if length <= 19 else "🍆"
            mention = "você" if name == ctx.author.name else f"@{name}"
            ctx.response = f"{mention} {length}cm {emoji}"

    @check(Checks.bot_has_role)
    @command(aliases=["sc", "cat"])
    @cooldown(rate=1, per=10)
    @helper(description="Receba a foto de um gatinho triste")
    async def sadcat(self, ctx: Context) -> None:
        sadcat = await self.api.sadcat()
        if sadcat:
            ctx.response = f"{sadcat} 😿"

    @command()
    @cooldown(rate=1, per=10)
    @helper(description="Dê um tapa em alguém do chat", usage="digite o comando e o nome de alguém que mereça levar uns tapas")
    async def slap(self, ctx: Context, name: str) -> None:
        name = username(name)
        if name == self.bot.nick:
            ctx.response = "vai bater na mãe 😠"
        elif name == ctx.author.name:
            ctx.response = "você se deu um tapa... 😕"
        else:
            ctx.response = f"você deu um tapa em @{name} 👋"

    @command()
    @cooldown(rate=1, per=10)
    @helper(description="Coloque alguém do chat na cama para dormir", usage="digite o comando e o nome de alguém para colocá-lo na cama")
    async def tuck(self, ctx: Context, name: str) -> None:
        name = username(name)
        if name == self.bot.nick:
            ctx.response = "eu não posso dormir agora..."
        elif name == ctx.author.name:
            ctx.response = "você foi para a cama"
        else:
            ctx.response = f"você colocou @{name} na cama 🙂👉🛏"


def prepare(bot: Bot) -> None:
    api = Api(config.api_key)
    bot.add_cog(FunCog(bot, api=api))
