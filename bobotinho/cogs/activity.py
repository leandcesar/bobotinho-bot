# -*- coding: utf-8 -*-
import json
from dataclasses import dataclass
from datetime import datetime

from bobotinho.bot import Bot, Context, Message, command, commands
from bobotinho.models import Afk, User


def to_username(name: str) -> str:
    return name.lstrip("@").rstrip(",").lower() if name else ""


@dataclass
class Status:
    _name: str
    _emoji: str
    _current: str
    _leave: str
    _leave_again: str
    _returned: str

    @property
    def current(self) -> str:
        return f"está {self._current}"

    @property
    def leave(self) -> str:
        return f"você {self._leave}"

    @property
    def leave_again(self) -> str:
        return f"você continuou {self._leave_again}"

    @property
    def returned(self) -> str:
        return f"você {self._returned}"


class Activity(commands.Cog):
    status = {
        "afk": Status("afk", "🏃⌨", "ficou AFK", "AFK", "voltou", "AFK"),
        "art": Status("art", "🎨", "foi desenhar", "desenhando", "desenhou", "desenhando"),
        "brb": Status("brb", "🏃⌨", "volta já", "fora", "voltou", "fora"),
        "code": Status("code", "💻", "foi programar", "programando", "programou", "programando"),
        "food": Status("food", "🍽", "foi comer", "comendo", "comeu", "comendo"),
        "game": Status("game", "🎮", "foi jogar", "jogando", "jogou", "jogando"),
        "gn": Status("gn", "💤", "foi dormir", "dormindo", "acordou", "dormindo"),
        "read": Status("read", "📖", "foi ler", "lendo", "leu", "lendo"),
        "shower": Status("shower", "🚿", "foi pro banho", "no banho", "tomou banho", "o banho"),
        "study": Status("study", "📚", "foi estudar", "estudando", "estudou", "estudando"),
        "watch": Status("watch", "📺", "foi assistir", "assistindo", "assistiu", "assistindo"),
        "work": Status("work", "💼", "foi trabalhar", "trabalhando", "trabalhou", "trabalhando"),
    }

    def __init__(self, bot: Bot) -> None:
        self.bot = bot

    @command(aliases=[s for s in status if s != "afk"])
    async def afk(self, ctx: Context, *, content: str = "") -> None:
        status = self.status[ctx.alias]
        await Afk.create(user_id=ctx.author.id, alias=ctx.alias, content=content)
        ctx.response = f"{status.leave}: {content or status.emoji}"

    @command(usage="digite o comando e o nome do usuário para saber se ele está AFK")
    async def isafk(self, ctx: Context, name: str) -> None:
        name = to_username(name)
        if name == self.bot.nick:
            ctx.response = "eu sempre estou aqui... observando"
        elif name == ctx.author.name:
            ctx.response = "você não está AFK... obviamente"
        elif user := await User.get_or_none(name=name):
            if afk := await Afk.get_or_none(user_id=user.id):
                status = self.status[afk.alias]
                ctx.response = f"@{name} {status.current}: {afk.content or status.emoji} ({afk.created_ago})"
            else:
                ctx.response = f"@{name} não está AFK"
        else:
            ctx.response = "esse usuário ainda não foi registrado (não usou nenhum comando)"

    @command(aliases=[f"r{s}" for s in status if s != "afk"])
    async def rafk(self, ctx: Context) -> None:
        afk_str = self.bot.cache.get(f"afk-{ctx.author.id}")
        if afk_str:
            self.bot.cache.delete(f"afk-{ctx.author.id}")
            status = self.status[ctx.alias[1:]]
            afk = json.loads(afk_str)
            content = afk.get("content")
            created_at = datetime.fromisoformat(afk.get("created_at"))
            await Afk.create(user_id=ctx.author.id, alias=ctx.alias[1:], content=content, created_at=created_at)
            ctx.response = f"{status.leave_again}: {content or status.emoji}"
        else:
            ctx.response = "digite o comando em até 2 minutos após ter retornado do seu AFK para retomá-lo"

    @commands.Cog.event("event_message")
    async def returned(self, message: Message) -> None:
        if message.echo:
            return None
        afk = await Afk.get_or_none(user_id=message.author.id)
        if afk is None:
            return None
        await afk.delete()
        if "afk" not in self.bot.channels[message.channel.name]["disabled"]:
            status = self.status[afk.alias]
            response = f"{status.returned}: {afk.content or status.emoji} ({afk.created_ago})"
            await message.channel.send(f"{message.author.name}, {response}")
        afk_str = json.dumps({"content": afk.content, "created_at": afk.created_at.isoformat()})
        self.bot.cache.set(f"afk-{message.author.id}", afk_str, ex=120)


def prepare(bot: Bot) -> None:
    bot.add_cog(Activity(bot))
