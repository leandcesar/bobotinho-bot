# -*- coding: utf-8 -*-
from bobotinho.apis import Color, Twitch
from bobotinho.bot import Bot, Context, command, commands
from bobotinho.models import User


def is_birthday(date: str) -> bool:
    return "ano" in date and not any(x in date for x in ["mês", "meses", "semana", "dia"])


def to_username(name: str) -> str:
    return name.lstrip("@").rstrip(",").lower() if name else ""


class Info(commands.Cog):

    def __init__(self, bot: Bot) -> None:
        self.bot = bot

    @command(aliases=["age"])
    async def accountage(self, ctx: Context, name: str = "") -> None:
        name = to_username(name) or ctx.author.name
        if name == self.bot.nick:
            ctx.response = "eu sempre existi..."
        else:
            age = await Twitch.age(name)
            mention = "você" if name == ctx.author.name else f"@{name}"
            if is_birthday(age):
                ctx.response = f"hoje completa {age.split()[0]} anos que {mention} criou a conta 🎂"
            else:
                ctx.response = f"{mention} criou a conta há {age}"

    @command(aliases=["icon"])
    async def avatar(self, ctx: Context, name: str = "") -> None:
        name = to_username(name) or ctx.author.name
        avatar = await Twitch.avatar(name)
        if name == ctx.author.name:
            ctx.response = f"sua foto de perfil: {avatar}"
        elif name == self.bot.nick:
            ctx.response = f"minha foto de perfil: {avatar}"
        else:
            ctx.response = f"foto de perfil de @{name}: {avatar}"

    @command(aliases=["colour"])
    async def color(self, ctx: Context, name: str = "") -> None:
        name = to_username(name) or ctx.author.name
        if name == self.bot.nick:
            ctx.response = "eu uso a cor #FFFFFF (White)"
        elif user := await User.get_or_none(name=name):
            mention = "você" if name == ctx.author.name else f"@{name}"
            ctx.response = f"{mention} usa a cor {user.color}"
            if color_name := await Color.name(user.color):
                ctx.response += f" ({color_name})"
            if user.saved_color:
                ctx.response += f" e salvou a cor {user.saved_color}"
        else:
            ctx.response = "esse usuário ainda não foi registrado (não usou nenhum comando)"

    @command(aliases=["create"])
    async def creation(self, ctx: Context, name: str = "") -> None:
        name = to_username(name) or ctx.author.name
        if name == self.bot.nick:
            ctx.response = "eu fui criado antes de tudo isso..."
        else:
            creation = await Twitch.creation(name)
            mention = "você" if name == ctx.author.name else f"@{name}"
            ctx.response = f"{mention} criou a conta em {creation}"

    @command(aliases=["ff"])
    async def firstfollow(self, ctx: Context, name: str = "") -> None:
        name = to_username(name) or ctx.author.name
        following = await Twitch.following(name)
        follower = await Twitch.follower(name)
        mention = "você" if name == ctx.author.name else f"@{name}"
        if following and follower:
            ctx.response = f"{mention} seguiu primeiro @{following} e foi seguido primeiro por @{follower}"
        elif following is None:
            ctx.response = f"{mention} não segue ninguém e foi seguido primeiro por @{follower}"
        elif following is None:
            ctx.response = f"{mention} seguiu primeiro @{following} e não é seguido por ninguém"
        else:
            ctx.response = f"{mention} não segue e não é seguido por ninguém"

    @command(aliases=["fa"])
    async def followage(self, ctx: Context, name: str = "", channel: str = "") -> None:
        name = to_username(name) or ctx.author.name
        channel = to_username(channel) or ctx.channel.name
        if name == self.bot.nick:
            ctx.response = "eu estou em todo lugar, desde sempre..."
        elif name == channel:
            ctx.response = "um usuário não pode se seguir"
        else:
            follow_age = await Twitch.follow_age(channel, name)
            name = "você" if name == ctx.author.name else f"@{name}"
            channel = "você" if channel == ctx.author.name else f"@{channel}"
            if follow_age is None:
                ctx.response = f"{name} não segue {channel}"
            elif is_birthday(follow_age):
                ctx.response = f"hoje completa {follow_age.split()[0]} anos que {name} segue {channel} 🎂"
            else:
                ctx.response = f"{name} segue {channel} há {follow_age}"

    @command()
    async def followed(self, ctx: Context, name: str = "", channel: str = "") -> None:
        name = to_username(name) or ctx.author.name
        channel = to_username(channel) or ctx.channel.name
        if name == self.bot.nick:
            ctx.response = "eu estou em todo lugar, desde sempre..."
        elif name == channel:
            ctx.response = "um usuário não pode se seguir"
        else:
            followed = await Twitch.followed(channel, name)
            name = "você" if name == ctx.author.name else f"@{name}"
            channel = "você" if channel == ctx.author.name else f"@{channel}"
            if followed is None:
                ctx.response = f"{name} não segue {channel}"
            else:
                ctx.response = f"{name} seguiu {channel} em {followed}"

    @command(aliases=["stream"])
    async def live(self, ctx: Context, channel: str = "") -> None:
        channel = to_username(channel) or ctx.channel.name
        uptime = await Twitch.uptime(channel)
        title = await Twitch.title(channel)
        game = await Twitch.game(channel)
        mention = "você" if channel == ctx.author.name else f"@{channel}"
        if channel == self.bot.nick:
            ctx.response = "eu sou um bot, não um streamer..."
        elif "is offline" in uptime and title:
            ctx.response = f"{mention} está offline: {title}"
        elif "is offline" in uptime:
            ctx.response = f"{mention} está offline"
        elif title and game:
            ctx.response = f"{mention} está streamando {game}: {title} ({uptime})"
        elif title:
            ctx.response = f"{mention} está online: {title} ({uptime})"
        elif game:
            ctx.response = f"{mention} está streamando {game} ({uptime})"
        else:
            ctx.response = f"{mention} está online ({uptime})"


def prepare(bot: Bot) -> None:
    bot.add_cog(Info(bot))
