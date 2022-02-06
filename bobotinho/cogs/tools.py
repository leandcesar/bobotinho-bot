# -*- coding: utf-8 -*-
import re

from bobotinho.apis import Currency, Math, Translator, Weather
from bobotinho.bot import Bot, Context, command, commands
from bobotinho.models import User


def as_currency(amount: float) -> str:
    return f"{amount:,.2f}".translate({44: 46, 46: 44})  # 1234567.89 -> "1.234.567,89"


class Tools(commands.Cog):

    def __init__(self, bot: Bot) -> None:
        self.bot = bot
        self.currency_api = Currency(key=bot.config.api.currency_key)
        self.weather_api = Weather(key=bot.config.api.weather_key)

    async def _to_brl(self, base: str, amount: float) -> str:
        conversion = await self.currency_api.convert(base, "BRL")
        total = amount * conversion
        return f"{as_currency(amount)} {base} = {as_currency(total)} BRL"

    @command(aliases=["crypto"], usage="digite o comando e a sigla da moeda ou crypto (ex: BTC)")
    async def currency(self, ctx: Context, coin: str, amount: float = 1.0) -> None:
        ctx.response = await self._to_brl(coin.upper(), amount)

    @command()
    async def bitcoin(self, ctx: Context, amount: float = 1.0) -> None:
        ctx.response = await self._to_brl("BTC", amount)

    @command()
    async def dolar(self, ctx: Context, amount: float = 1.0) -> None:
        ctx.response = await self._to_brl("USD", amount)

    @command()
    async def ethereum(self, ctx: Context, amount: float = 1.0) -> None:
        ctx.response = await self._to_brl("ETH", amount)

    @command()
    async def euro(self, ctx: Context, amount: float = 1.0) -> None:
        ctx.response = await self._to_brl("EUR", amount)

    @command(usage="digite o comando e uma operação matemática para eu resolvê-la")
    async def math(self, ctx: Context, *, expression: str) -> None:
        try:
            ctx.response = await Math.evaluate(expression)
        except Exception:
            ctx.response = (
                "não consegui calcular... lembre-se: use * para multiplicação, "
                "use / para divisão, e use ponto em vez de vírgula para números decimais"
            )

    @command(usage="digite o comando e uma frfase para traduzí-la")
    async def translate(self, ctx: Context, from_to: str, *, content: str = ""):
        match = re.match(r"(\w{2})?->(\w{2})?", from_to)  # e.g.: en->pt or en-> or ->pt
        if match:
            source, target = match.groups()
        else:
            content = f"{from_to} {content}"
            source = target = None
        try:
            ctx.response = Translator.translate(text=content, source=source or "auto", target=target or "pt")
        except Exception:
            ctx.response = "não foi possível traduzir isso"

    @command(aliases=["wt"])
    async def weather(self, ctx: Context, *, location: str = ""):
        if not location:
            user = await User.get(id=ctx.author.id)
            location = user.city
        if location and "," not in location and not location.endswith("br"):
            location = f"{location}, br"
        if location:
            try:
                weather = await self.weather_api.predict(location)
            except Exception:
                ctx.response = "não há nenhuma previsão para esse local"
            else:
                ctx.response = (
                    f"em {weather.city} ({weather.country}): {weather.status}, "
                    f"{weather.temp_now}°C (sensação de {weather.feels_like}°C), "
                    f"ventos a {weather.wind}m/s e {weather.humidity}% de umidade"
                )
        else:
            ctx.response = "digite o comando e o nome de um local para saber o clima"


def prepare(bot: Bot) -> None:
    bot.add_cog(Tools(bot))
