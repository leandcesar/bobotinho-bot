# -*- coding: utf-8 -*-
from datetime import datetime

from bobotinho import config
from bobotinho.api import Api
from bobotinho.commands import Bot, Checks, Cog, Context, check, command, helper
from bobotinho.database import Channel, User
from bobotinho.webhook import Webhook


class BasicCog(Cog):

    def __init__(self, bot: Bot, *, api: Api) -> None:
        self.bot = bot
        self.api = api
        self.boot = datetime.utcnow()

    @command(aliases=["bot", "info"])
    @helper(description="Veja as principais informações sobre o bot")
    async def botinfo(self, ctx: Context) -> None:
        ctx.response = (
            f"estou conectado à {len(self.bot.channels)} canais, "
            f"com {len(self.bot.commands)} comandos, "
            f"feito por @{config.dev} em Python e hospedado em Heroku"
        )

    @command()
    @helper(description="Reporte um bug que está ocorrendo no Bot", usage="digite o comando e o bug que você encontrou")
    async def bug(self, ctx: Context, *, content: str) -> None:
        data = await self.api.twitch("avatar", ctx.author.name)
        avatar_url = data["avatar"] if data and data.get("avatar") else None
        if await Webhook().discord(
            config.bugs_url,
            content=content,
            user_name=ctx.author.name,
            user_avatar_url=avatar_url,
        ):
            ctx.response = f"seu bug foi reportado 🐛"

    @check(Checks.bot_has_role)
    @command(aliases=["commands"])
    @helper(description="Receba o link da lista de comandos ou veja como utilizar um comando específico")
    async def help(self, ctx: Context, *, command_name: str = None) -> None:
        for command in self.bot.commands.values():
            if command_name == command.name or (command.aliases and command_name in command.aliases):
                if command.aliases:
                    aliases = ", ".join([ctx.prefix + alias for alias in command.aliases])
                    ctx.response = f"{ctx.prefix}{command.name} ({aliases}): {command.description}"
                else:
                    ctx.response = f"{ctx.prefix}{command.name}: {command.description}"
                break
        else:
            ctx.response = f"veja todos os comandos: {config.site_url}/docs/help"

    @check(Checks.bot_has_role)
    @command()
    @helper(description="Receba o link para adicionar o bot no seu chat")
    async def invite(self, ctx: Context) -> None:
        ctx.response = f"me adicione no seu chat: {config.site_url}/invite"

    @command()
    @helper(description="Verifique se o bot está online")
    async def ping(self, ctx: Context) -> None:
        delta = datetime.utcnow() - ctx.message.timestamp
        ctx.response = f"ping 🏓 {delta.microseconds / 1000}ms"

    @check(Checks.bot_has_role)
    @command(aliases=["discord", "github", "twitter"])
    @helper(description="Receba o link do site do Bot para mais informações")
    async def site(self, ctx: Context) -> None:
        ctx.response = f"acesse: {config.site_url}/"

    @command(aliases=["suggestion"])
    @helper(description="Faça uma sugestão de recurso para o bot", usage="digite o comando e uma sugestão de recurso ou modificação para o bot")
    async def suggest(self, ctx: Context, *, content: str) -> None:
        data = await self.api.twitch("avatar", ctx.author.name)
        avatar_url = data["avatar"] if data and data.get("avatar") else None
        if await Webhook().discord(
            config.suggestions_url,
            content=content,
            user_name=ctx.author.name,
            user_avatar_url=avatar_url,
        ):
            ctx.response = f"sua sugestão foi anotada 💡"

    @command()
    @helper(description="Verifique há quanto tempo o bot está online")
    async def uptime(self, ctx: Context) -> None:
        uptime = datetime.utcnow() - self.boot
        minutes, seconds = divmod(int(uptime.total_seconds()), 60)
        hours, minutes = divmod(m, 60)
        ctx.response = f"eu estou ligado há"
        ctx.response += f" {hours}h" if hours else ""
        ctx.response += f" {minutes}min" if minutes else ""
        ctx.response += f" {seconds}s" if seconds else ""


def prepare(bot: Bot) -> None:
    api = Api(config.api_key)
    bot.add_cog(BasicCog(bot, api=api))
