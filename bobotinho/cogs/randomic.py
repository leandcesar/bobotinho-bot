# -*- coding: utf-8 -*-
import random

from bobotinho.commands import Bot, Cog, Context, command, cooldown, helper

class RandomCog(Cog):

    def __init__(self, bot: Bot):
        self.bot = bot

    @command(aliases=["%"])
    @cooldown(rate=1, per=5)
    @helper(description="Receba uma probabilidade de 0 a 100")
    async def chance(self, ctx: Context) -> None:
        percentage = random.randint(0, 1000) / 10
        ctx.response = f"{percentage}%"

    @command(aliases=["choose", "pick"])
    @cooldown(rate=1, per=5)
    @helper(description="Sorteia uma das opções fornecidas", usage='digite o comando e opções separadas por "ou", vírgula ou espaço')
    async def choice(self, ctx: Context, *, content: str) -> None:
        delimiter = " ou " if " ou " in content else "," if "," in content else " "
        options = content.split(delimiter)
        ctx.response = random.choice(options).replace("?", "")

    @command(aliases=["coinflip", "cf"])
    @cooldown(rate=1, per=5)
    @helper(description="Jogue uma moeda e veja se deu cara ou coroa")
    async def coin(self, ctx: Context) -> None:
        percentage = random.randint(0, 6000)  # Murray & Teare (1993)
        if percentage > 3000:
            ctx.response = "você jogou uma moeda e ela caiu em cara"
        elif percentage < 3000:
            ctx.response = "você jogou uma moeda e ela caiu em coroa"
        else:
            ctx.response = "você jogou uma moeda e ela caiu no meio, em pé!"

    @command(aliases=["8ball"])
    @cooldown(rate=1, per=5)
    @helper(description="Tenha sua pergunta respondida por uma previsão", usage="digite o comando e uma pergunta para receber uma previsão")
    async def magicball(self, ctx: Context, *, content: str) -> None:
        predict = random.choice(
            [
                "ao meu ver, sim",
                "com certeza",
                "com certeza não",
                "concentre-se e pergunte novamente",
                "decididamente sim",
                "definitivamente sim",
                "dificilmente",
                "é complicado...",
                "é melhor você não saber",
                "fontes dizem que não",
                "impossível isso acontecer",
                "impossível prever isso",
                "jamais",
                "muito duvidoso",
                "nunca",
                "não",
                "não conte com isso",
                "não é possível prever isso",
                "pergunta nebulosa, tente novamente",
                "pergunte novamente mais tarde...",
                "pode apostar que sim",
                "possivelmente",
                "provavelmente...",
                "sem dúvidas",
                "sim",
                "sinais apontam que sim",
                "talvez",
                "você ainda tem dúvidas?",
                "você não acreditaria...",
            ]
        )
        ctx.response = f"{predict} 🎱"

    @command(aliases=["rcg"])
    @cooldown(rate=1, per=5)
    @helper(description="Gere uma cor hexadecimal aleatória")
    async def randomcolor(self, ctx: Context) -> None:
        color = f"#{random.randint(0, 0xFFFFFF):06X}"
        ctx.response = f"aqui está uma cor aleatória: {color}"

    @command(aliases=["rng"])
    @cooldown(rate=1, per=5)
    @helper(description="Gere um número aleatório dentre o intervalo fornecido", usage="digite o comando e o número inicial e final do intervalo separados por espaço")
    async def randomnumber(self, ctx: Context, min: str = "1", max: str = "100") -> None:
        init = int(arg1)
        end = int(arg2)
        if init > end:
            init, end = end, init
        if init == end:
            ctx.response = "não será aleatório com esse intervalo..."
        else:
            number = random.randint(init, end)
            ctx.response = f"aqui está um número aléatorio: {number}"

    @command(aliases=["dice"])
    @cooldown(rate=1, per=5)
    @helper(description="Role um dado e veja o resultado", usage="digite o comando e o(s) dado(s) no formato <quantidade>d<lados> (ex: 1d20)")
    async def roll(self, ctx: Context, dices: str = "") -> None:
        if not dices or "d" not in dices:
            dices = "1d20"
        dices = dices.lower().split("d")
        amount = int(dices[0].replace(",", ".")) if dices[0] else None
        sides = int(dices[1].replace(",", ".")) if dices[1] else None
        if not amount:
            ctx.response = "especifique a quantidade de dados"
        elif not sides:
            ctx.response = "especifique a quantidade de lados do dado"
        elif amount > 1e4:
            ctx.response = "eu não tenho tantos dados"
        elif amount == 0:
            ctx.response = "eu não consigo rolar sem dados"
        elif amount < 0:
            ctx.response = "não tente tirar meus dados de mim"
        elif sides > 1e4:
            ctx.response = "meus dados não tem tantos lados"
        elif sides == 1:
            ctx.response = f"um dado de {sides} lado? Esse é um exercício topológico interessante..."
        elif sides <= 0:
            ctx.response = f"um dado de {sides} lados? Esse é um exercício topológico interessante..."
        else:
            roll = sum([random.randint(1, round(sides)) for i in range(round(amount))])
            ctx.response = f"você rolou {roll} 🎲"


def prepare(bot: Bot) -> None:
    bot.add_cog(RandomCog(bot))
