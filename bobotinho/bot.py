# -*- coding: utf-8 -*-
import inspect
from typing import Optional

from twitchio.ext.commands import (
    Bot,
    Bucket,
    Command,
    Context,
    Cooldown,
)
from twitchio.ext.commands.errors import (
    CheckFailed,
    CommandNotFound,
    CommandOnCooldown,
    MissingRequiredArgument,
)
from twitchio.message import Message

from bobotinho import log
from bobotinho.apis import Analytics
from bobotinho.database.models import Channel, User
from bobotinho.exceptions import (
    BotOffline,
    CommandDisabled,
    InappropriateMessage,
    AlreadyPlaying,
    InvalidUser,
    UserNotAllowed,
)
from bobotinho.utils import convert

DEFAULT_COOLDOWN_RATE = 2
DEFAULT_COOLDOWN_PER = 5
DEFAULT_COOLDOWN_BUCKET = Bucket.user


class Ctx(Context):
    def __init__(self, message: Message, bot: Bot, **kwargs) -> None:
        super().__init__(message, bot, **kwargs)
        self.response: Optional[str] = None
        self.user: User = None

    def __iter__(self):
        yield "author", getattr(self.author, "name", None)
        yield "channel", getattr(self.channel, "name", None)
        yield "user", getattr(self.user, "id", None)
        yield "message", getattr(self.message, "content", None)
        yield "response", self.response


class Role:
    @staticmethod
    def dev(ctx: Ctx) -> bool:
        return ctx.author.name == ctx.bot.config.dev

    @staticmethod
    def owner(ctx: Ctx) -> bool:
        return ctx.author.name == ctx.channel.name

    @staticmethod
    def admin(ctx: Ctx) -> bool:
        return ctx.author.is_mod or Role.owner(ctx) or Role.dev(ctx)

    @staticmethod
    def vip(ctx: Ctx) -> bool:
        return ctx.author.badges and bool(ctx.author.badges.get("vip"))

    @staticmethod
    def sub(ctx: Ctx) -> bool:
        return ctx.author.is_subscriber

    @staticmethod
    def sponsor(ctx) -> bool:
        return ctx.user and ctx.user.sponsor

    @staticmethod
    def any(ctx: Ctx) -> bool:
        return (
            Role.sub(ctx)
            or Role.vip(ctx)
            or Role.admin(ctx)
            or Role.owner(ctx)
            or Role.dev(ctx)
            or Role.sponsor(ctx)
        )


class Check:
    @staticmethod
    def allowed(ctx: Ctx) -> bool:
        if not Role.any(ctx) and convert.str2url(ctx.message.content) is not None:
            raise UserNotAllowed
        return True

    @staticmethod
    def banword(ctx: Ctx) -> bool:
        if any(word in ctx.message.content for word in ctx.bot.channels[ctx.channel.name]["banwords"]):
            raise InappropriateMessage
        return True

    @staticmethod
    def enabled(ctx: Ctx) -> bool:
        if ctx.command.name in ctx.bot.channels[ctx.channel.name]["disabled"]:
            raise CommandDisabled
        return True

    @staticmethod
    def game(ctx: Ctx) -> bool:
        if ctx.bot.cache.get(f"game-{ctx.channel.name}"):
            raise AlreadyPlaying
        return True

    @staticmethod
    def online(ctx: Ctx) -> bool:
        if not ctx.bot.channels[ctx.channel.name]["online"]:
            raise BotOffline
        return True


class TwitchBot(Bot):
    def __init__(self, config):
        super().__init__(
            token=config.access_token,
            client_secret=config.client_secret,
            prefix=config.prefix,
            case_insensitive=True,
        )
        self.config = config
        self.blocked = []
        self.listeners = []
        self.routines = []
        self.channels = {}
        self.cache = None
        self.analytics = Analytics(config.api.analytics_key)

    async def start(self) -> None:
        await self.connect()
        await self.add_all_channels()
        await self.fetch_blocked()

    async def stop(self) -> None:
        [routine.stop() for routine in self.routines]
        await self.close()

    def add_checks(self) -> None:
        global_checks = [Check.online, Check.enabled, Check.banword]
        [self.check(check) for check in global_checks]

    def add_channel(self, name, id, banwords=[], disabled=[], online=True) -> None:
        if name in self.channels:
            log.warning(f"'{name}' already added")
        else:
            self.channels[name] = {
                "id": id, "banwords": banwords, "disabled": disabled, "online": online
            }

    async def add_all_channels(self) -> None:
        channels = await Channel.all().select_related("user")
        if not channels:
            self.add_channel(self.dev.lower(), 0)
        for channel in channels:
            if channel.user.block:
                continue
            self.add_channel(
                channel.user.name,
                channel.user_id,
                list(channel.banwords.keys()),
                list(channel.disabled.keys()),
                channel.online,
            )

    async def fetch_blocked(self) -> None:
        self.blocked = await User.filter(block=True).all().values_list("id", flat=True)

    async def reply(self, ctx: Ctx) -> bool:
        if not ctx.response:
            return False
        try:
            ctx.response = f"{ctx.user or ctx.author.name}, {ctx.response}"
            await ctx.send(ctx.response)
        except Exception as e:
            log.error(e, extra={"ctx": dict(ctx)})
        else:
            log.info(f"#{ctx.channel.name} @{self.nick}: {ctx.response}")
            await self.analytics.sent(
                author_id=ctx.author.id,
                author_name=ctx.author.name,
                channel_name=ctx.channel.name,
                message=ctx.response,
            )
            return True
        return False

    async def handle_commands(self, ctx: Ctx) -> bool:
        if ctx.response:
            return False
        if not ctx.prefix:
            return False
        if not ctx.is_valid:
            return False
        log.info(f"#{ctx.channel.name} @{ctx.author.name}: {ctx.message.content}")
        self.analytics.received(
            author_id=ctx.author.id,
            author_name=ctx.author.name,
            channel_name=ctx.channel.name,
            message=ctx.message.content,
        )
        if not ctx.user:
            ctx.user, _ = await User.get_or_create(
                id=ctx.author.id,
                defaults={
                    "channel": ctx.channel.name,
                    "name": ctx.author.name,
                    "color": ctx.author.colour,
                    "content": ctx.message.content.replace("ACTION", "", 1),
                },
            )
        try:
            await self.invoke(ctx)
        except MissingRequiredArgument:
            ctx.response = ctx.command.usage
        except Exception as e:
            log.error(e, extra={"ctx": dict(ctx)})
        return await self.reply(ctx)

    async def handle_listeners(self, ctx: Ctx) -> bool:
        for listener in self.listeners:
            if ctx.response:
                break
            if inspect.iscoroutinefunction(listener):
                await listener(ctx)
            else:
                listener(ctx)
        return await self.reply(ctx)

    async def event_ready(self) -> None:
        log.info(f"{self.nick} | #{len(self.channels)} | {self._prefix}{len(self.commands)}")

    async def event_raw_data(self, data) -> None:
        bot_part_prefix = f":{self.nick}!{self.nick}@{self.nick}.tmi.twitch.tv PART"
        if data.startswith(f"{bot_part_prefix} #"):
            i = len(f"{bot_part_prefix} #")
            channel = data[i:].strip("\r\n")
            self._connection._cache.pop(channel)

    async def event_command_error(self, ctx: Ctx, e: Exception) -> None:
        if isinstance(e, CommandDisabled):
            ctx.response = "esse comando está desativado nesse canal"
        elif isinstance(e, InappropriateMessage):
            ctx.response = "sua mensagem contém um termo banido"
        elif isinstance(e, UserNotAllowed):
            ctx.response = "apenas inscritos, VIPs e MODs podem enviar links"
        elif isinstance(e, InvalidUser):
            ctx.response = "nome de usuário inválido"
        elif isinstance(e, AlreadyPlaying):
            ctx.response = "um jogo já está em andamento nesse canal"
        elif isinstance(e, (BotOffline, CommandOnCooldown, CommandNotFound, CheckFailed)):
            log.info(e)
        else:
            ctx.response = "ocorreu um erro inesperado"
            log.error(e, extra={"ctx": dict(ctx)}, exc_info=e)
        await self.reply(ctx)

    async def event_message(self, message: Message) -> None:
        if message.echo:
            return
        if message.author.id in self.blocked:
            return
        if not self.channels[message.channel.name]["online"] and message.content != f"{self._prefix}start":
            return
        ctx: Ctx = await self.get_context(message, cls=Ctx)
        ctx.user = await User.update_or_none(ctx)
        await self.handle_listeners(ctx)
        await self.handle_commands(ctx)
