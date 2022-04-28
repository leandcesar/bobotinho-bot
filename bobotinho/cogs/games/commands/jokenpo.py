# -*- coding: utf-8 -*-
import random

description = "Tente vencer no pedra, papel e tesoura"
aliases = ["jokempo"]
usage = 'digite o comando e "pedra", "papel" ou "tesoura"'


async def command(ctx, arg: str):
    arg = (
        "pedra"
        if arg == "✊"
        else "papel"
        if arg == "✋"
        else "tesoura"
        if arg in ("✌️", "✌")
        else arg
    )
    choice = random.choice(["papel", "pedra", "tesoura"])
    if arg == choice:
        ctx.response = f"eu também escolhi {choice}, nós empatamos..."
    elif (arg, choice) in [("pedra", "papel"), ("papel", "tesoura"), ("tesoura", "pedra")]:
        ctx.response = f"eu escolhi {choice} e consegui te prever facilmente"
    elif (choice, arg) in [("pedra", "papel"), ("papel", "tesoura"), ("tesoura", "pedra")]:
        ctx.response = f"eu escolhi {choice}, você deu sorte dessa vez"
