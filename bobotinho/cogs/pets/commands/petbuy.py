# -*- coding: utf-8 -*-
from bobotinho.cogs.pets import random_pets
from bobotinho.models import Cookie, Pet

description = "Adquira um dos pets disponíveis na loja"
usage = "digite o comando e um dos pets disponíveis na loja para adquirí-lo"


async def command(ctx, arg: str):
    if pet := random_pets().get(arg.lower()):
        if cookie := await Cookie.get_or_none(id=ctx.author.id):
            if await Pet.filter(user_id=ctx.author.id).count() >= 3:
                ctx.response = "você já possui a quantidade máxima de pets"
            elif cookie.stocked < pet.price:
                ctx.response = f"estoque {pet.price} cookies para adquirir {pet.specie} {pet.emoji}"
            else:
                await Pet.create(user_id=ctx.author.id, specie=pet.specie)
                await cookie.stock(-pet.price)
                ctx.response = f"você adquiriu {pet.specie} {pet.emoji}, agora escolha o nome!"
        else:
            ctx.response = f'comece a estocar cookies para adquirir um pet ("{ctx.prefix}stock")'
    else:
        ctx.response = f'escolha um dos pets disponíveis na lista de hoje ("{ctx.prefix}petlist")'
