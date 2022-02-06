# -*- coding: utf-8 -*-
from bobotinho.bot import Bot, Context, command, commands
from bobotinho.models import Cookie, User, Wedding


def to_username(name: str) -> str:
    return name.lstrip("@").rstrip(",").lower() if name else ""


class Weddings(commands.Cog):

    def __init__(self, bot: Bot) -> None:
        self.bot = bot

    async def cog_check(self, ctx: Context) -> bool:
        if not await Cookie.exists(id=ctx.author.id):
            await Cookie.create(id=ctx.author.id, name=ctx.author.name)
        return True

    @command(usage="digite o comando e o nome de quem você quer pedir em casamento")
    async def marry(self, ctx: Context, name: str) -> None:
        # TODO: otimizar a quantidade de consultas no banco e os if/else
        name = to_username(name)
        if name == ctx.bot.nick:
            ctx.response = "não fui programado para fazer parte de um relacionamento"
        elif name == ctx.author.name:
            ctx.response = "você não pode se casar com você mesmo..."
        elif not (user_2 := await User.get_or_none(name=name)):
            ctx.response = f"@{name} ainda não foi registrado (não usou nenhum comando)"
        elif someone := ctx.bot.cache.get(f"marry-{ctx.author.name}"):
            ctx.response = (
                f"antes você precisa responder ao pedido de @{someone}! "
                f'Digite "{ctx.prefix}yes" ou "{ctx.prefix}no"'
            )
        elif someone := ctx.bot.cache.get(f"marry-{name}"):
            ctx.response = f"@{someone} chegou primeiro e já fez uma proposta à mão de @{name}"
        elif len(await Wedding.find_all(ctx.author.id)) >= (1 + int((await User.get(id=ctx.author.id)).sponsor)):
            ctx.response = "você já está com o número máximo de relacionamentos, não é o suficiente?"
        elif await Wedding.find(ctx.author.id, user_2.id):
            ctx.response = "vocês dois já são casados... não se lembra?"
        elif len(await Wedding.find_all(user_2.id)) >= (1 + int(user_2.sponsor)):
            ctx.response = f"@{name} já está com o número máximo de relacionamentos, não há espaço para mais um..."
        elif (await Cookie.get(name=ctx.author.name)).stocked < 100:
            ctx.response = "para pagar a aliança e todo o casório, você deve ter 100 cookies estocados"
        else:
            ctx.bot.cache.set(f"marry-{name}", ctx.author.name, ex=180)
            ctx.response = (
                f"você pediu a mão de @{name}, o usuário deve "
                f'digitar "{ctx.prefix}yes" ou "{ctx.prefix}no" 💐💍'
            )

    @command(usage="digite o comando e o nome da pessoa com quem se casou para se divorciar")
    async def divorce(self, ctx: Context, name: str) -> None:
        name = to_username(name)
        if name == ctx.bot.nick:
            ctx.response = "eu nunca estaria casado com você"
        elif name == ctx.author.name:
            ctx.response = "você não pode se livrar de você mesmo"
        elif not await Wedding.find(ctx.author.id):
            ctx.response = "você não está casado com ninguém"
        elif not (user := await User.get_or_none(name=name)):
            ctx.response = f"@{name} ainda não foi registrado (não usou nenhum comando)"
        elif wedding := await Wedding.find(ctx.author.id, user.id):
            await wedding.divorce()
            ctx.response = (
                "então, é isso... da próxima vez, case-se com alguém "
                "que realmente te ame, e não qualquer pessoa por aí"
            )
        else:
            ctx.response = "você não sabe nem o nome da pessoa com quem está casado?"

    @command(usage="digite o comando e o nome da pessoa com quem se casou para se divorciar")
    async def marriage(self, ctx: Context, name: str) -> None:
        name = to_username(name) or ctx.author.name
        mention = "você" if name == ctx.author.name else f"@{name}"
        if name == ctx.bot.nick:
            ctx.response = "nunca me casarei com ninguém"
        elif not (user := await User.get_or_none(name=name)):
            ctx.response = f"@{name} ainda não foi registrado (não usou nenhum comando)"
        elif (weddings := await Wedding.find_all(user.id)):
            users = [await wedding.spouse(name) for wedding in weddings]
            timeago = [wedding.created_ago for wedding in weddings]
            if len(weddings) == 1:
                ctx.response = f"{mention} está casado com @{users[0].name} há {timeago[0]}"
            else:
                ctx.response = (
                    f"{mention} está casado com @{users[0].name} há {timeago[0]} e "
                    f"com @{users[1].name} há {timeago[1]}"
                )
        else:
            ctx.response = f"{mention} não está casado com ninguém"


def prepare(bot: Bot) -> None:
    bot.add_cog(Weddings(bot))
