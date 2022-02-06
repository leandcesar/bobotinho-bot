# -*- coding: utf-8 -*-
from bobotinho.cogs.pets import all_pets
from bobotinho.models import Cookie, Pet

description = "Devolva um pet em troca de parte da quantia que gastou"
usage = "digite o comando e o nome ou espécie do pet que quer devolver"


async def command(ctx, *, content: str):
    if pet := await Pet.find(id=ctx.author.id, name=content.title(), specie=content.lower()):
        price = round(all_pets[pet.specie].price * 0.7)
        emoji = all_pets[pet.specie].emoji
        cookie = await Cookie.get(id=ctx.author.id)
        cookie.stocked += price
        await cookie.save()
        await pet.delete()
        ctx.response = f"você devolveu {pet} {emoji} em troca de {price} cookies"
    else:
        ctx.response = f'adquira um pet em troca de cookies ("{ctx.prefix}petlist")'
