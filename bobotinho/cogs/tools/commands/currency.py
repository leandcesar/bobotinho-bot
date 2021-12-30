# -*- coding: utf-8 -*-
from bobotinho.apis import Currency
from bobotinho.utils import convert

description = "Saiba o valor da conversão de uma moeda em reais"
aliases = ["dolar", "euro", "libra"]
usage = "digite o comando, a sigla (ex: USD) e a quantidade para saber a conversão em reais"


async def command(ctx, arg1: str = "", arg2: str = ""):
    translate = {"dolar": "USD", "euro": "EUR", "libra": "GBP"}
    invoke_by = ctx.message.content.partition(" ")[0][len(ctx.prefix):].lower()
    target = "BRL"
    base = translate.get(invoke_by) or arg1.upper()
    amount = convert.str2float(arg1) or convert.str2float(arg2) or 1.0
    conversion = await Currency(ctx.bot.config.apis.currency_key).convert(base, target)
    total = amount * conversion
    amount = convert.number2str(amount)
    total = convert.number2str(total)
    ctx.response = f"{amount} {base} = {total} {target}"
