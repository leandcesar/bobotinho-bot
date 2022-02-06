# -*- coding: utf-8 -*-
from bobotinho.cogs.pets import join_pets
from bobotinho.cogs.pets.commands import petbuy, petlist, petname, petpat, petsell
from bobotinho.models import Pet, User
from bobotinho.utils import convert

description = "Veja os pets de um usuário"
aliases = ["pets"]


async def command(ctx, arg: str = "", *, content: str = ""):
    name = convert.str2name(arg, default=ctx.author.name)
    mention = "você" if name == ctx.author.name else f"@{name}"
    if arg == "buy":
        await petbuy.command(ctx, arg=content)
    elif arg == "list":
        await petlist.command(ctx)
    elif arg == "name":
        await petname.command(ctx, content=content)
    elif arg == "pat":
        await petpat.command(ctx)
    elif arg == "sell":
        await petsell.command(ctx, content=content)
    elif not (user := await User.get_or_none(name=name)):
        ctx.response = f"@{name} ainda não foi registrado (não usou nenhum comando)"
    elif arg and not user.mention:
        ctx.response = "esse usuário optou por não permitir mencioná-lo"
    elif pets := await Pet.filter(user_id=user.id).all():
        ctx.response = f'{mention} possui {join_pets(pets, formatter="{pet} {emoji}")}'
    elif name == ctx.author.name:
        ctx.response = f'adquira um pet em troca de cookies ("{ctx.prefix}petlist")'
    else:
        ctx.response = f"{mention} não possui um pet"
