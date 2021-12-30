# -*- coding: utf-8 -*-
from bobotinho.apis import Math

description = "Saiba o resultado de alguma expressão matemática"
usage = "digite o comando e uma expressão matemática (ex: 1+1)"


async def command(ctx, *, content: str):
    try:
        response = await Math.evaluate(content)
        ctx.response = response.replace("Infinity", "infinito").replace("NaN", "🤯")
    except Exception:
        ctx.response = (
            "não consegui calcular isso... lembre-se: use * para multiplicação, "
            "use / para divisão, e use ponto em vez de vírgula para números decimais"
        )
