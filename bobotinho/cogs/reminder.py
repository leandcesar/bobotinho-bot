# -*- coding: utf-8 -*-
import asyncio
import re
from datetime import datetime, timedelta
from typing import Optional

from bobotinho.apis import Wit
from bobotinho.bot import Bot, Context, Message, command, commands, routines
from bobotinho.models import Reminder, User

PATTERN_TIME = re.compile(
    r"""
    (\b(?P<years>\d+)\s?(?:anos|ano|a|years|year|y)\b\s?)?
    (\b(?P<months>\d+)\s?(?:meses|mês|mes|months|month|mo)\b\s?)?
    (\b(?P<weeks>\d+)\s?(?:semanas|semana|weeks|week|w)\b\s?)?
    (\b(?P<days>\d+)\s?(?:dias|dia|d|days|day)\b\s?)?
    (\b(?P<hours>\d+)\s?(?:horas|hora|h|hours|hour)\b\s?)?
    (\b(?P<minutes>\d+)\s?(?:minutos|minuto|min|m|minutes|minute)\b\s?)?
    (\b(?P<seconds>\d+)\s?(?:segundos|segundo|seg|s|seconds|second|secs|sec)\b\s?)?
    """,
    re.VERBOSE,
)


def find_time(content: str) -> Optional[re.Match]:
    match = PATTERN_TIME.match(content)
    return match if match and any(match.groups()) else None


def from_match_to_datetime(match: re.Match) -> datetime:
    match_dict = match.groupdict()
    delta = timedelta(
        weeks=match_dict.get("weeks", 0),
        days=365 * match_dict.get("years", 0) + 30.4 * match_dict.get("months", 0) + match_dict.get("days", 0),
        hours=match_dict.get("hours", 0),
        minutes=match_dict.get("minutes", 0),
        seconds=match_dict.get("seconds", 0),
    )
    return datetime.now() + delta


def to_username(name: str) -> str:
    return name.lstrip("@").rstrip(",").lower() if name else ""


class Rememberer(commands.Cog):

    def __init__(self, bot: Bot) -> None:
        self.bot = bot
        self.wit = Wit(token=bot.config.api.wit_token)

    @commands.cooldown(rate=2, per=15)
    @command(aliases=["remember"], usage="digite o comando, o usuário e um texto para o lembrete")
    async def remind(self, ctx: Context, name: str, *, content: str) -> None:
        name = ctx.author.name if name == "me" else to_username(name)
        mention = "você" if name == ctx.author.name else f"@{name}"
        user = await User.get_or_none(name=name)
        if name == self.bot.nick:
            ctx.response = "estou sempre aqui... não precisa me deixar lembretes"
        elif await Reminder.filter(from_user_id=ctx.author.id).count() > 10:
            ctx.response = "já existem muitos lembretes seus pendentes..."
        elif not user:
            ctx.response = "esse usuário ainda não foi registrado (não usou nenhum comando)"
        elif await Reminder.filter(from_user_id=user.id, scheduled_for__isnull=True).count() > 10:
            ctx.response = f"já existem muitos lembretes pendentes para {mention}"
        elif content.startswith("in "):
            ctx.response = (
                f'em vez de "{self.bot.prefix}remind {name} in 10min...", '
                f'use {self.bot.prefix}timer {name} 10min...'
            )
        elif content.startswith("on "):
            ctx.response = (
                f'em vez de "{self.bot.prefix}remind {name} on 31/12...", '
                f'use {self.bot.prefix}timer {name} 31/12...'
            )
        else:
            remind = await Reminder.create(
                from_user_id=ctx.author.id,
                to_user_id=user.id,
                channel_id=self.bot.channels[ctx.channel.name]["id"],
                content=content,
            )
            ctx.response = f"{mention} será lembrado disso na próxima vez que falar no chat 📝 (ID {remind.id})"

    @commands.cooldown(rate=2, per=15)
    @command(usage="digite o comando, o usuário, o tempo e um texto para o timer")
    async def timer(self, ctx: Context, name: str, *, content: str) -> None:
        name = ctx.author.name if name == "me" else to_username(name)
        mention = "você" if name == ctx.author.name else f"@{name}"
        user = await User.get_or_none(name=name)
        if name == self.bot.nick:
            ctx.response = "estou sempre aqui... não precisa me deixar lembretes"
        elif await Reminder.filter(from_user_id=ctx.author.id).count() > 10:
            ctx.response = "já existem muitos lembretes seus pendentes..."
        elif not user:
            ctx.response = "esse usuário ainda não foi registrado (não usou nenhum comando)"
        elif await Reminder.filter(from_user_id=user.id, scheduled_for__isnull=True).count() > 10:
            ctx.response = f"já existem muitos lembretes pendentes para {mention}"
        else:
            match = find_time(content[3:])
            scheduled_for = from_match_to_datetime(match)
            if scheduled_for <= datetime.now():
                ctx.response = "eu ainda não inventei a máquina do tempo"
            elif datetime.now() - scheduled_for < 59:
                ctx.response = "o tempo mínimo para lembretes cronometrados é 1 minuto"
            else:
                content = content.lstrip(match.group(0))
                remind = await Reminder.create(
                    from_user_id=ctx.author.id,
                    to_user_id=user.id,
                    channel_id=self.bot.channels[ctx.channel.name]["id"],
                    content=content,
                    scheduled_for=scheduled_for,
                )
                ctx.response = f"{mention} será lembrado disso daqui {remind.scheduled_to} ⏲️ (ID {remind.id})"

    @commands.cooldown(rate=2, per=15)
    @command(usage="digite o comando, o usuário, a data e um texto para o agendamento")
    async def schedule(self, ctx: Context, name: str, *, content: str) -> None:
        name = ctx.author.name if name == "me" else to_username(name)
        mention = "você" if name == ctx.author.name else f"@{name}"
        user = await User.get_or_none(name=name)
        if name == self.bot.nick:
            ctx.response = "estou sempre aqui... não precisa me deixar lembretes"
        elif await Reminder.filter(from_user_id=ctx.author.id).count() > 10:
            ctx.response = "já existem muitos lembretes seus pendentes..."
        elif not user:
            ctx.response = "esse usuário ainda não foi registrado (não usou nenhum comando)"
        elif await Reminder.filter(from_user_id=user.id, scheduled_for__isnull=True).count() > 10:
            ctx.response = f"já existem muitos lembretes pendentes para {mention}"
        else:
            entity = await self.wit.detect(content)
            scheduled_for = datetime.fromisoformat(entity["value"])
            if scheduled_for <= datetime.now():
                ctx.response = "eu ainda não inventei a máquina do tempo"
            elif datetime.now() - scheduled_for < 59:
                ctx.response = "o tempo mínimo para lembretes cronometrados é 1 minuto"
            else:
                content = content.lstrip(entity["body"])
                remind = await Reminder.create(
                    from_user_id=ctx.author.id,
                    to_user_id=user.id,
                    channel_id=ctx.bot.channels[ctx.channel.name]["id"],
                    content=content,
                    scheduled_for=scheduled_for,
                )
                ctx.response = f"{mention} será lembrado disso em {remind.scheduled_for} 📅 (ID {remind.id})"

    @command()
    async def reminds(self, ctx: Context, arg: str = "", id: str = "") -> None:
        if arg.isdecimal() and (remind := await Reminder.filter(id=int(arg), from_user_id=ctx.author.id).first()):
            await remind.fetch_related("to_user")
            mention = "você" if remind.to_user.name == ctx.author.name else f"@{remind.to_user.name}"
            if remind.scheduled_for:
                ctx.response = f"esse lembrete é para {mention} em {remind.scheduled_for}: {remind.content}"
            else:
                ctx.response = f"esse lembrete é para {mention}: {remind.content}"
        elif (
            arg.lower() == "delete"
            and id.isdecimal()
            and (remind := await Reminder.filter(id=int(id), from_user_id=ctx.author.id).first())
        ):
            await remind.delete()
            ctx.response = f"seu lembrete de ID {remind.id} foi deletado"
        elif arg.isdecimal() or (arg.lower() == "delete" and id.isdecimal()):
            ctx.response = "você não possui nenhum lembrete com esse ID"
        elif arg.lower() == "delete":
            ctx.response = "você deve passar o ID do lembrete que quer deletar"
        if reminds := await Reminder.filter(from_user_id=ctx.author.id).order_by("id").all():
            reminds_id = ", ".join([str(remind.id) for remind in reminds])
            ctx.response = f"seus lembretes pendentes são os de ID: {reminds_id}"
        else:
            ctx.response = "você não tem lembretes pendentes"

    @commands.Cog.event("event_message")
    async def returned(self, message: Message) -> None:
        if message.echo:
            return None
        remind = (
            await Reminder.filter(to_user_id=message.author.id, scheduled_for=None)
            .order_by("created_at")
            .first()
        )
        if remind is None or "remind" in self.bot.channels[message.channel.name]["disabled"]:
            return None
        from_user = await User.get_or_none(id=remind.from_user_id)
        await remind.delete()
        mention = "você" if remind.from_user_id == message.author.id else f"@{from_user.name}"
        content = remind.content or ""
        response = f"{mention} deixou um lembrete: {content} ({remind.created_ago})"
        await message.channel.send(f"{message.author.name}, {response}")

    @routines.routine(seconds=30)
    async def scheduled(self) -> None:
        reminds = await Reminder.filter(
            scheduled_for__not_isnull=True,
            scheduled_for__lt=datetime.now() + timedelta(seconds=30),
        ).order_by("scheduled_for").all()
        for remind in reminds:
            await remind.fetch_related("from_user", "to_user", "channel")
            mention = "você" if remind.from_user_id == remind.to_user_id else f"@{remind.from_user.name}"
            if "remind" in self.bot.channels[remind.channel.name]["disabled"]:
                continue
            if not self.bot.channels[remind.channel.name]["online"]:
                continue
            delta = remind.scheduled_to.total_seconds()
            if delta > 0:
                await asyncio.sleep(delta, loop=self.bot.loop)
            try:
                if remind.content:
                    response = f"{mention} deixou um lembrete: {remind.content} ({remind.created_ago})"
                else:
                    response = f"{mention} deixou um lembrete em branco ({remind.created_ago})"
                channel = self.bot.get_channel(remind.channel.name)
                await channel.send(f"{remind.to_user}, {response}")
            except Exception:
                continue
            else:
                await remind.delete()


def prepare(bot: Bot) -> None:
    bot.add_cog(Rememberer(bot))
