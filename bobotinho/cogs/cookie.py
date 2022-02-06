# -*- coding: utf-8 -*-
import random

from bobotinho.bot import Bot, Context, command, commands
from bobotinho.models import Cookie, User


def random_file_line(filename: str) -> str:
    with open(filename, "r", encoding="utf-8") as file:
        lines = file.read().splitlines()
    return random.choice(lines)


def to_username(name: str) -> str:
    return name.lstrip("@").rstrip(",").lower() if name else ""


class Cookies(commands.Cog):

    def __init__(self, bot: Bot) -> None:
        self.bot = bot

    async def cog_check(self, ctx: Context) -> bool:
        if not await Cookie.exists(id=ctx.author.id):
            await Cookie.create(id=ctx.author.id, name=ctx.author.name)
        return True

    @command()
    async def cookie(self, ctx: Context, amount: str = "1") -> None:
        try:
            amount = int(amount)
        except Exception:
            amount = 1
        cookie = await Cookie.get(id=ctx.author.id)
        if amount == 0:
            ctx.response = "você não comeu nada, uau!"
        elif amount < 0:
            ctx.response = f"para comer {amount} cookies, você primeiro deve saber reverter a entropia"
        elif cookie.stocked + cookie.daily >= amount:
            await cookie.consume(amount)
            if amount > 1:
                ctx.response = f"você comeu {amount} cookies de uma só vez 🥠"
            else:
                filename = "bobotinho//data//cookies.txt"
                ctx.response = f"{random_file_line(filename)} 🥠"
        elif amount > 1:
            ctx.response = f"você não tem {amount} cookies estocados para comer"
        else:
            ctx.response = "você já usou seu cookie diário, a próxima fornada sai às 6 da manhã! ⌛"

    @command(aliases=["cc"])
    async def cookiecount(self, ctx: Context, name: str = "") -> None:
        name = to_username(name) or ctx.author.name
        mention = "você" if name == ctx.author.name else f"@{name}"
        cookie = await Cookie.get_or_none(name=name)
        if name == ctx.bot.nick:
            ctx.response = "eu tenho cookies infinitos, e distribuo uma fração deles para vocês"
        elif cookie:
            ctx.response = (
                f"{mention} já comeu {cookie.count} cookies, presenteou {cookie.donated}, "
                f"foi presenteado com {cookie.received} e tem {cookie.stocked} estocados"
            )
        else:
            ctx.response = f"{mention} ainda não comeu nenhum cookie"

    @command(aliases=["give"], usage="digite o comando e um usuário para presentear com seu cookie")
    async def gift(self, ctx: Context, name: str = "") -> None:
        name = to_username(name) or ctx.author.name
        cookie_from = await Cookie.get(id=ctx.author.id)
        user = await User.get_or_none(name=name)
        if name == ctx.bot.nick:
            ctx.response = "eu não quero seu cookie"
        elif name == ctx.author.name:
            ctx.response = "você presenteou você mesmo, uau!"
        elif not user:
            ctx.response = f"@{name} ainda não foi registrado (não usou nenhum comando)"
        elif cookie_from.daily >= 1:
            cookie_to, _ = await Cookie.get_or_create(name=name)
            await cookie_from.donate()
            await cookie_to.receive()
            ctx.response = f"você presenteou @{name} com um cookie 🎁"
        else:
            ctx.response = "você já usou seu cookie diário, a próxima fornada sai às 6 da manhã! ⌛"

    @command(aliases=["sm"])
    async def slotmachine(self, ctx: Context) -> None:
        cookie = await Cookie.get(id=ctx.author.id)
        if cookie.daily >= 1:
            x, y, z = random.choices("🍇🍊🍋🍒🍉🍐", k=3)
            await cookie.use_daily()
            if x == y == z:
                await cookie.stock(10)
                ctx.response = f"[{x}{y}{z}] você usou seu cookie diário e ganhou 10 cookies! PogChamp"
            elif x == y or x == z or y == z:
                await cookie.stock(3)
                ctx.response = f"[{x}{y}{z}] você usou seu cookie diário e ganhou 3 cookies!"
            else:
                ctx.response = f"[{x}{y}{z}] você perdeu seu cookie diário..."
        else:
            ctx.response = "você já usou seu cookie diário, a próxima fornada sai às 6 da manhã! ⌛"

    @command()
    async def stock(self, ctx: Context) -> None:
        cookie = await Cookie.get(id=ctx.author.id)
        if cookie.daily >= 1:
            await cookie.use_daily()
            await cookie.stock()
            ctx.response = "você estocou seu cookie diário"
        else:
            ctx.response = "você já usou seu cookie diário, a próxima fornada sai às 6 da manhã! ⌛"

    @command()
    async def top(self, ctx: Context, order_by: str = "count") -> None:
        order_by, title = (
            ("donated", "givers")
            if order_by in ("gift", "gifts", "give", "gives", "giver", "givers")
            else ("count", "cookiers")
        )
        cookies = await Cookie.filter().order_by(f"-{order_by}").limit(5).all()
        emojis = "🏆🥈🥉🏅🏅"
        tops = " ".join(
            [
                f"{emoji} @{cookie.name} ({getattr(cookie, order_by)})"
                for emoji, cookie in zip(emojis, cookies)
            ]
        )
        ctx.response = f"top {len(cookies)} {title}: {tops}"


def prepare(bot: Bot) -> None:
    bot.add_cog(Cookies(bot))
