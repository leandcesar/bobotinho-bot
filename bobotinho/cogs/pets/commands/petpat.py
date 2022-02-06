# -*- coding: utf-8 -*-
from bobotinho.cogs.pets import join_pets
from bobotinho.models import Pet

description = "Faça carinho nos seus pets"


async def command(ctx):
    if all_pets := await Pet.filter(user_id=ctx.author.id).all():
        pets = join_pets(all_pets, formatter="{pet} {emoji}")
        ctx.response = f"você fez carinho em {pets}"
    else:
        ctx.response = f'adquira um pet em troca de cookies ("{ctx.prefix}petlist")'
