# -*- coding: utf-8 -*-
from bobotinho.database import Cookie

description = "Veja quais sÃ£o os maiores comedores ou doadores de cookies"


async def command(ctx, arg: str = ""):
    if arg in ["gift", "gifts", "give", "gives", "giver", "givers"]:
        order_by, title = "donated", "givers"
    else:
        order_by, title = "count", "cookiers"
    cookies = await Cookie.filter().order_by("-"+order_by).limit(5).all()
    emojis = "ðð¥ð¥ðð"
    tops = " ".join(
        [
            f"{emoji} @{cookie.name} ({getattr(cookie, order_by)})"
            for emoji, cookie in zip(emojis, cookies)
        ]
    )
    ctx.response = f"top {len(cookies)} {title}: {tops}"
