# -*- coding: utf-8 -*-
from bobotinho.cogs.pets import all_pets
from bobotinho.models import Pet

description = "Dê um nome para o seu pet"
usage = "digite o comando e o nome que desejar para seu pet"


async def command(ctx, *, content: str):
    pets = await Pet.filter(user_id=ctx.author.id).all()
    num = 0
    if len(pets) > 1 and " " in content:
        specie, name = content.split(maxsplit=1)
        specie = specie.lower()
        name = name.title()
        if " " in name and name.split(maxsplit=1)[0] in ("1", "2", "3"):
            num, name = name.split(maxsplit=1)
            num = int(num) - 1
    elif len(pets) == 1:
        specie = pets[0].specie
        name = content.title()
    if len(pets) == 0:
        ctx.response = f'adquira um pet em troca de cookies ("{ctx.prefix}petlist")'
    elif len(pets) > 1 and (" " not in content or not any([specie == pet.specie for pet in pets])):
        ctx.response = (
            "você tem mais de um pet, então passe a espécie e depois o nome "
            f'(pets da mesma espécie? Use: "{ctx.prefix}petname <espécie> <1,2,3> <nome>"'
        )
    elif len(name) > 32:
        ctx.response = "esse nome é muito comprido para seu pet"
    elif not all(char.isalpha() or char.isspace() for char in name):
        ctx.response = "esse nome não é válido (apenas letras e espaços)"
    else:
        pet = await Pet.filter(user_id=ctx.author.id, specie=specie).offset(num).first()
        pet.name = name
        await pet.save()
        ctx.response = f"agora seu pet se chama {name} {all_pets[specie].emoji}"
