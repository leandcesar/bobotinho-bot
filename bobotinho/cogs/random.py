# -*- coding: utf-8 -*-
import random

from bobotinho.bot import Bot, Context, command, commands


def random_file_line(filename: str) -> str:
    with open(filename, "r", encoding="utf-8") as file:
        lines = file.read().splitlines()
    return random.choice(lines)


class Random(commands.Cog):

    def __init__(self, bot: Bot) -> None:
        self.bot = bot

    @commands.cooldown(rate=2, per=15)
    @command(aliases=["%"])
    async def chance(self, ctx: Context) -> None:
        ctx.response = f"{random.random() * 100:.2f}%"

    @commands.cooldown(rate=2, per=15)
    @command(aliases=["choose", "pick"], usage="digite o comando e opções para eu escolher uma")
    async def choice(self, ctx: Context, *, content: str) -> None:
        separator = " ou " if " ou " in content else ", " if ", " in content else " "
        options = content.split(separator)
        ctx.response = random.choice(options).replace("?", "")

    @commands.cooldown(rate=2, per=15)
    @command(aliases=["coin", "cf"])
    async def coinflip(self, ctx: Context) -> None:
        percentage = random.randint(0, 6000)  # Murray & Teare (1993)
        ctx.response = (
            "você jogou uma moeda e ela caiu em cara"
            if percentage > 3000
            else "você jogou uma moeda e ela caiu em coroa"
            if percentage < 3000
            else "você jogou uma moeda e ela caiu no meio, em pé!"
        )

    @commands.cooldown(rate=2, per=15)
    @command(aliases=["4head", "hahaa"])
    async def joke(self, ctx: Context):
        filename = "bobotinho//data//jokes.txt"
        ctx.response = f"{random_file_line(filename)} 4Head"

    @commands.cooldown(rate=2, per=15)
    @command(aliases=["jokempo"], usage="digite o comando e a sua escolha (pedra, papel ou tesoura)")
    async def jokenpo(self, ctx: Context, choice: str):
        choice = (
            "pedra"
            if choice in ("pedra", "✊")
            else "papel"
            if choice in ("papel", "✋")
            else "tesoura"
            if choice in ("tesoura", "✌️", "✌")
            else None
        )
        result = random.choice([-1, 0, 1])
        if choice is None:
            ctx.response = "escolha pedra, papel ou tesoura"
        elif result == 0:
            ctx.response = f"eu também escolhi {choice}, nós empatamos..."
        elif result == -1:
            win = {"pedra": "papel", "papel": "tesoura", "tesoura": "pedra"}
            ctx.response = f"eu escolhi {win.get(choice)} e consegui te prever facilmente"
        elif result == 1:
            lose = {"pedra": "tesoura", "papel": "pedra", "tesoura": "papel"}
            ctx.response = f"eu escolhi {lose.get(choice)}, você deu sorte dessa vez"

    @commands.cooldown(rate=2, per=15)
    @command(aliases=["8ball"])
    async def magicball(self, ctx: Context) -> None:
        filename = "bobotinho//data//magicball.txt"
        ctx.response = f"{random_file_line(filename)} 🎱"

    @commands.cooldown(rate=2, per=15)
    @command()
    async def penis(self, ctx: Context) -> None:
        length = int(ctx.author.id) % 30
        emoji = "🍆" if length >= 20 else "🍌" if length >= 15 else "🪱" if length >= 10 else "🤏"
        ctx.response = f"{length if length > 6 else 6}cm {emoji}"

    @commands.cooldown(rate=2, per=15)
    @command(aliases=["rsc", "sadcat"])
    async def randomsadcat(self, ctx: Context) -> None:
        filename = "bobotinho//data//sadcats.txt"
        ctx.response = f"https://i.imgur.com/{random_file_line(filename)} 😿"

    @commands.cooldown(rate=2, per=15)
    @command(aliases=["rc"])
    async def randomcolor(self, ctx: Context) -> None:
        ctx.response = f"aqui está uma cor aleatória: #{random.randint(0, 0xFFFFFF):06X}"

    @commands.cooldown(rate=2, per=15)
    @command(aliases=["rng"])
    async def randomnumber(self, ctx: Context, start: str = "0", stop: str = "100") -> None:
        try:
            start, stop = float(start), float(stop)
        except Exception:
            start, stop = 0.0, 100.0
        if start > stop:
            ctx.response = "o valor inicial do intervalo deve ser menor que o valor final"
        elif start == stop:
            ctx.response = "não será aleatório se você já souber o resultado..."
        else:
            ctx.response = f"aqui está um número aléatorio: {random.randrange(start, stop)}"

    @commands.cooldown(rate=2, per=15)
    @command()
    async def roll(self, ctx: Context, dice: str = "1d20") -> None:
        try:
            rolls, limit = map(int, dice.split("d"))
        except Exception:
            rolls = limit = None
        if rolls is None or limit is None:
            ctx.response = "o dado deve estar no formato <dados>d<lados> (por exemplo, 1d20)"
        elif rolls > 1e4:
            ctx.response = "eu não tenho tantos dados"
        elif rolls == 0:
            ctx.response = "eu não consigo rolar sem dados"
        elif rolls < 0:
            ctx.response = "não tente tirar dados de mim"
        elif limit > 1e4:
            ctx.response = "meus dados não tem tantos lados"
        elif limit <= 1:
            ctx.response = f"um dado de {limit} lado(s)? Esse é um exercício topológico interessante..."
        else:
            ctx.response = f"sua rolada deu {sum([random.randint(1, limit) for _ in range(rolls)])} 🎲"


def prepare(bot: Bot) -> None:
    bot.add_cog(Random(bot))
