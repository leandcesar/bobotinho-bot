# -*- coding: utf-8 -*-
from bobotinho.models import Player

description = "Saiba quais são os melhores jogadores da dungeon"


async def command(ctx, arg: str = ""):
    order_by, title, class_ = (
        ("wins", "vitórias", None)
        if arg in ["vitoria", "vitorias", "vitória", "vitórias", "win", "wins"]
        else ("defeats", "derrotas", None)
        if arg in ["derrota", "derrotas", "lose", "losses"]
        else ("level", "guerreiros", "w")
        if arg in ["guerreiro", "guerreiros", "guerreira", "guerreiras"]
        else ("level", "magos", "m")
        if arg in ["mago", "magos", "maga", "magas"]
        else ("level", "arqueiros", "a")
        if arg in ["arqueiro", "arqueiros", "arqueira", "arqueiras"]
        else ("level", "dungeons", None)
    )
    players = (
        await Player.filter(class_=class_).order_by(f"-{order_by}", "-xp").limit(5).all()
        if class_
        else await Player.filter().order_by(f"-{order_by}", "-xp").limit(5).all()
    )
    emojis = "🏆🥈🥉🏅🏅"
    tops = " ".join(
        [
            f"{emoji} @{player.name} ({getattr(player, order_by)})"
            for emoji, player in zip(emojis, players)
        ]
    )
    ctx.response = f"top {len(players)} {title}: {tops}"
