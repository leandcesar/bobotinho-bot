# -*- coding: utf-8 -*-
import re

from emoji import demojize

from bobotinho.bot import Bot, Context, command, commands, exceptions
from bobotinho.models import User


def demoji(text: str) -> str:
    emoji = demojize(text)
    return emoji if emoji != text and emoji.count(":") == 2 else ""


def is_hex(color: str) -> str:
    match = re.match(r"^#?([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$", color)
    return f"#{match.group(1).lower()}" if match else ""


class Profile(commands.Cog):

    def __init__(self, bot: Bot) -> None:
        self.bot = bot

    async def cog_check(self, ctx: Context) -> bool:
        if not await User.get(id=ctx.author.id).values_list("sponsor", flat=True):
            raise exceptions.PremiumRequired
        return True

    @command(usage="digite o comando e um emoji para usar como badge")
    async def savebadge(self, ctx: Context, *, emoji: str) -> None:
        badge = "" if emoji == "delete" else demoji(emoji)
        await User.filter(id=ctx.author.id).update(badge=badge)
        ctx.response = "você alterou sua badge de apoiador"

    @command()
    async def savecolor(self, ctx: Context, *, color: str = "") -> None:
        hex_code = is_hex(color) or ctx.author.colour
        await User.filter(id=ctx.author.id).update(saved_color=hex_code)
        ctx.response = (f'você salvou a cor {hex_code.upper()} e pode visualizá-la usando "{ctx.prefix}color"')

    @command(aliases=["savelocation"], usage="digite o comando e o nome da cidade que deseja salvar")
    async def savecity(self, ctx: Context, *, content: str) -> None:
        city = content.title()
        await User.filter(id=ctx.author.id).update(city=city)
        ctx.response = f"você salvou {city} como sua cidade, agora basta usar {ctx.prefix}weather"

    @command()
    async def mention(self, ctx: Context) -> None:
        await User.filter(id=ctx.author.id).update(mention=True)
        ctx.response = "outros usuários poderão mencionar você novamente nos comandos"

    @command()
    async def unmention(self, ctx: Context) -> None:
        await User.filter(id=ctx.author.id).update(mention=False)
        ctx.response = "agora outros usuários não poderão mais mencionar você nos comandos"


def prepare(bot: Bot) -> None:
    bot.add_cog(Profile(bot))
