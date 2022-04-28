# -*- coding: utf-8 -*-
from bobotinho import config
from bobotinho.api import Api
from bobotinho.commands import Bot, Checks, Cog, Context, check, command, cooldown, helper
from bobotinho.exceptions import InvalidName


def username(name: str) -> str:
    if name[0] == "@":
        name = name[1:]
    if name[-1] == ",":
        name = name[:-1]
    if not name.replace("_", "").isalnum():
        raise InvalidName()
    return name.lower()


class TwitchCog(Cog):

    def __init__(self, bot: Bot, *, api: Api):
        self.bot = bot
        self.api = api

    @command(aliases=["age"])
    @cooldown(rate=1, per=5)
    @helper(description="Saiba há quanto tempo algum usuário criou sua conta")
    async def accountage(self, ctx: Context, name: str = None) -> None:
        name = ctx.author.name if name is None else username(name)
        if name == self.bot.nick:
            ctx.response = "eu sempre existi..."
        else:
            data = await self.api.twitch("account_age", name)
            mention = "você" if name == ctx.author.name else f"@{name}"
            if data and data["account_age"]:
                account_age = data["account_age"]
                ctx.response = f"{mention} criou a conta há {account_age}"
            else:
                ctx.response = f"{mention} não existe"

    @check(Checks.bot_has_role)
    @command(aliases=["icon"])
    @cooldown(rate=1, per=5)
    @helper(description="Receba o link da foto de perfil de algum usuário")
    async def avatar(self, ctx: Context, name: str = None) -> None:
        name = ctx.author.name if name is None else username(name)
        data = await self.api.twitch("avatar", name)
        if data and data["avatar"]:
            avatar = data["avatar"]
            if name == ctx.author.name:
                ctx.response = f"sua foto de perfil: {avatar}"
            elif name == self.bot.nick:
                ctx.response = f"minha foto de perfil: {avatar}"
            else:
                ctx.response = f"foto de perfil de @{name}: {avatar}"
        else:
            ctx.response = f"{mention} não existe"

    @command(aliases=["create"])
    @cooldown(rate=1, per=5)
    @helper(description="Saiba quando algum usuário criou sua conta")
    async def creation(self, ctx: Context, name: str = None) -> None:
        name = ctx.author.name if name is None else username(name)
        if name == self.bot.nick:
            ctx.response = "eu sempre existi..."
        else:
            data = await self.api.twitch("creation", name)
            mention = "você" if name == ctx.author.name else f"@{name}"
            if data and data["creation"]:
                creation = data["creation"]
                ctx.response = f"{mention} criou a conta em {creation}"
            else:
                ctx.response = f"{mention} não existe"

    @command(aliases=["fa"])
    @cooldown(rate=1, per=5)
    @helper(description="Saiba há quanto tempo algum usuário segue algum canal")
    async def followage(self, ctx: Context, name: str = None, channel: str = None) -> None:
        name = ctx.author.name if name is None else username(name)
        channel = ctx.channel.name if name is None else username(channel)
        mention = "você" if name == ctx.author.name else f"@{name}"
        mention_channel = "você" if channel == ctx.author.name else f"@{channel}"
        if name == channel:
            ctx.response = f"{mention} não pode se seguir"
        elif channel == self.bot.nick:
            ctx.response = f"{mention} nunca consegueria me seguir"
        elif name == self.bot.nick:
            ctx.response = f"eu sempre estive em {mention_channel}..."
        else:
            data = await self.api.twitch("follow_age", channel, name)
            if data and data["follow_age"] and not "não segue" in data["follow_age"]:
                follow_age = data["follow_age"]
                ctx.response = f"{mention} segue {mention_channel} há {follow_age}"
            else:
                ctx.response = f"{mention} não segue {mention_channel}"

    @command()
    @cooldown(rate=1, per=5)
    @helper(description="Saiba quando algum usuário segue algum canal")
    async def followed(self, ctx: Context, name: str = None, channel: str = None) -> None:
        name = ctx.author.name if name is None else username(name)
        channel = ctx.channel.name if name is None else username(channel)
        mention = "você" if name == ctx.author.name else f"@{name}"
        mention_channel = "você" if channel == ctx.author.name else f"@{channel}"
        if name == channel:
            ctx.response = f"{mention} não pode se seguir"
        elif name == self.bot.nick:
            ctx.response = f"eu sempre estive em {mention_channel}..."
        elif channel == self.bot.nick:
            ctx.response = f"{mention} nunca consegueria me seguir"
        else:
            data = await self.api.twitch("followed", channel, name)
            if data and data["followed"] and not "não segue" in data["followed"]:
                followed = data["followed"]
                ctx.response = f"{mention} segue {mention_channel} há {followed}"
            else:
                ctx.response = f"{mention} não segue {mention_channel}"

    @command(aliases=["stream"])
    @cooldown(rate=1, per=5)
    @helper(description="Veja as informações da live de algum canal")
    async def live(self, ctx: Context, name: str = None) -> None:
        name = ctx.author.name if name is None else username(name)
        if name == self.bot.nick:
            ctx.response = "eu sou um bot, não um streamer"
        else:
            data = await self.api.twitch("game,title,total_views,uptime,viewers", name)
            mention = "você" if name == ctx.author.name else f"@{name}"
            if data and (data["title"] or data["uptime"]):
                game = data["game"]
                title = data["title"]
                uptime = data["uptime"]
                if not uptime or "offline" in uptime:
                    ctx.response = f"{mention} está offline"
                elif game:
                    ctx.response = f"{mention} está streamando {game}"
                else:
                    ctx.response = f"{mention} está online"
                if title:
                    ctx.response += f": {title}"
                if uptime and "offline" not in uptime:
                    ctx.response += f" ({uptime})"
            else:
                ctx.response = f"{mention} não existe"


def prepare(bot: Bot) -> None:
    api = Api(config.api_key)
    bot.add_cog(TwitchCog(bot, api=api))
