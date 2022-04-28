# -*- coding: utf-8 -*-
import re

from bobotinho import config
from bobotinho.api import Api
from bobotinho.commands import Bot, Cog, Context, command, cooldown, helper


def to_float(number: str) -> float:
    try:
        return float(number.replace(",", "."))
    except Exception:
        return None


def to_str(number: float) -> str:
    try:
        return f"{target:,d}".replace(",", ".")
    except Exception:
        return f"{target:,.2f}"[::-1].replace(",", ".").replace(".", ",", 1)[::-1]


class ToolCog(Cog):

    def __init__(self, bot: Bot, *, api: Api):
        self.bot = bot
        self.api = api

    @command(aliases=["crypto", "dolar", "euro", "libra", "bitcoin", "ethereum"])
    @cooldown(rate=1, per=5)
    @helper(
        description="Saiba o valor da conversão de uma moeda em reais",
        usage="digite o comando, a sigla da moeda (ex: USD, BTC) e a quantidade para saber a conversão em reais",
    )
    async def currency(self, ctx: Context, base: str = "", amount: str = "") -> None:
        invoke_by = ctx.message.content.partition(" ")[0][len(ctx.prefix):].lower()
        aliases = {"dolar": "USD", "euro": "EUR", "libra": "GBP", "bitcoin": "BTC", "ethereum": "ETH"}
        if invoke_by in aliases:
            base = aliases.get(invoke_by)
            amount = to_float(base) or 1.0
        else:
            base = base.upper()
            amount = to_float(amount) or 1.0
        conversion = await self.api.currency(base, target="BRL")
        total = amount * float(conversion)
        amount = to_str(amount)
        total = to_str(total)
        ctx.response = f"{base} {amount} = {target} {total}"

    @command(aliases=["calculate"])
    @cooldown(rate=1, per=5)
    @helper(description="Saiba o resultado de alguma expressão matemática", usage="digite o comando e uma expressão matemática (ex: 1+1)")
    async def math(self, ctx: Context, *, content: str) -> None:
        try:
            result = await self.api.math(content)
            ctx.response = result.replace("Infinity", "infinito").replace("NaN", "🤯")
        except Exception:
            ctx.response = (
                "não consegui calcular isso... lembre-se: use * para multiplicação, "
                "use / para divisão, e use ponto em vez de vírgula para números decimais"
            )

    @command(aliases=["tr"])
    @cooldown(rate=1, per=5)
    @helper(description="Saiba a tradução de alguma mensagem", usage="digite o comando e um texto para ser traduzido")
    async def translate(self, ctx: Context, languages: str, *, content: str = "") -> None:
        if match := re.match(r"(\w{2})?->(\w{2})?", languages):  # source->target or source-> or ->target
            source, target = match.groups()
        else:
            content = f"{languages} {content}"
            source = target = None
        translation = await self.api.translate(content, source if source else "auto", target if target else "pt")
        if translation and translation != content:
            ctx.response = translation
        else:
            ctx.response = "não foi possível traduzir isso"

    @command(aliases=["wt"])
    @cooldown(rate=1, per=5)
    @helper(description="Saiba o clima atual de alguma cidade", usage="digite o comando e o nome de um local para saber o clima")
    async def weather(self, ctx: Context, *, content: str = "") -> None:
        place = content or ctx.user.city
        if place in ("salvador", "socorro", "santiago"):
            place = f"{place}, br"
        if place:
            try:
                weather = await self.api.weather(place)
                city = weather["name"]
                country = weather["country"]
                status = weather["description"]
                temperature = weather["temp"]
                feels_like = weather["temp_feels_like"]
                wind = weather["speed"]
                humidiy = weather["humidity"]
                emoji = weather["emoji"]
                ctx.response = (
                    f"em {city} ({country}): {status} {emoji}, {temperature}°C (sensação de "
                    f"{feels_like}°C), ventos a {wind}m/s e {humidiy}% de umidade"
                )
            except Exception:
                ctx.response = "não há nenhuma previsão para esse local"
        else:
            ctx.response = "digite o comando e o nome de um local para saber o clima"


def prepare(bot: Bot) -> None:
    api = Api(config.api_key)
    bot.add_cog(ToolCog(bot, api=api))
