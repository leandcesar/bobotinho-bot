# -*- coding: utf-8 -*-
from bobotinho.cogs.dungeons import (
    choose_class,
    choose_sub_class,
    classes,
    generate_dungeon,
    options_sub_class,
    resume_dungeon,
)
from bobotinho.models import Player
from bobotinho.utils import timetools

description = "Entre na dungeon, faça sua escolha e adquira experiência"
aliases = ["ed"]


async def command(ctx, *, content: str = ""):
    choice = content.lower()
    if player := await Player.get_or_none(id=ctx.author.id):
        if not player.sub_class:
            if sub_class := choose_sub_class(choice, player.class_, player.gender):
                player.sub_class = sub_class
                c = classes[player.class_][player.gender][player.sub_class][player.level//10]
                await player.save()
                ctx.response = f"agora você é {c}"
            else:
                option1, option2 = options_sub_class(player.class_, player.gender)
                ctx.response = (
                    f"antes de continuar, digite o comando e sua nova classe: {option1} ou {option2}"
                )
        elif player.dungeon:
            if choice and choice.split()[0] in ["1", "2"]:
                multiplier = 2 if ctx.user.sponsor else 1
                player, ctx.response = resume_dungeon(player, choice.split()[0], multiplier=multiplier)
                await player.save()
                ctx.response = response
            else:
                ctx.response = generate_dungeon(player.dungeon)[0]["quote"]
        elif cooldown := timetools.on_cooldown(player.updated_ago, s=10800):
            ctx.response = f"aguarde {cooldown} para entrar em outra dungeon ⌛"
        else:
            d, player.dungeon = generate_dungeon()
            await player.save()
            ctx.response = d["quote"]
    elif c := choose_class(choice):
        player = await Player.create(
            id=ctx.author.id,
            name=ctx.author.name,
            class_=c["class_"],
            gender=c["gender"],
            dungeon=generate_dungeon()[1],
        )
        emoji = classes[player.class_]["emoji"]
        ctx.response = f"você escolheu {choice.title()}! {emoji}"
    else:
        ctx.response = (
            "antes de continuar, escolha sua classe! "
            "Digite o comando e: Guerreiro(a), Arqueiro(a) ou Mago(a)"
        )
