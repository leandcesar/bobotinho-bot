# -*- coding: utf-8 -*-
import json
import os
from typing import Callable

from redis import Redis
from tortoise import Tortoise
from twitchio.ext import commands
from twitchio.ext import routines
from twitchio.message import Message

from bobotinho import exceptions
from bobotinho import log
from bobotinho.apis import Analytics
from bobotinho.cache import TTLOrderedDict
from bobotinho.config import Config
from bobotinho.models import Channel, User


def command(aliases: list = None, usage: str = None) -> Callable[[Callable], commands.Command]:

    def decorator(func: Callable) -> commands.Command:
        command = commands.Command(name=func.__name__, func=func, aliases=aliases)
        command.usage = usage
        return command

    return decorator


class Context(commands.Context):
    def __init__(self, message: Message, bot: commands.Bot, **attrs) -> None:
        super().__init__(message, bot, **attrs)
        self.response = ""

    def __iter__(self):
        yield "author", getattr(self.author, "name", None)
        yield "channel", getattr(self.channel, "name", None)
        yield "message", getattr(self.message, "content", None)

    @property
    def alias(self) -> str:
        return self.message.content.split()[0].lstrip(self.bot.prefix).lower()


class Bot(commands.Bot):
    def __init__(self, config: Config):
        super().__init__(
            token=config.token,
            client_secret=config.secret,
            prefix=config.prefix,
            case_insensitive=True,
        )
        self.config = config
        self.ignore = []
        self.channels = {}
        self.cache = None
        self.analytics = None

    @property
    def prefix(self) -> str:
        return self._prefix

    @routines.routine(seconds=15)
    async def check_channels(self) -> None:
        connected = [channel.name for channel in self.connected_channels]
        disconnected = [channel for channel in self.channels.keys() if channel not in connected]
        try:
            await self.join_channels(disconnected)
        except Exception as e:
            log.exception(e)

    @routines.routine(seconds=15)
    async def new_channels(self) -> None:
        new_channels = self.cache.getset("new-channels", "") or ""
        for new_channel in new_channels.split("\n"):
            if not new_channel:
                continue
            try:
                new_channel = json.loads(new_channel)
                user, _ = await User.update_or_create(
                    id=int(new_channel["id"]),
                    defaults={"name": new_channel["name"]},
                )
                channel, _ = await Channel.update_or_create(
                    user_id=user.id,
                    defaults={"followers": new_channel["followers"]},
                )
                if channel.user.block:
                    continue
                self.channels[channel.user.name] = {
                    "id": channel.user_id,
                    "banwords": list(channel.banwords.keys()),
                    "disabled": list(channel.disabled.keys()),
                    "online": channel.online,
                }
            except Exception as e:
                log.exception(e)

    def init_analytics(self) -> None:
        if self.config.api.analytics_key:
            self.analytics = Analytics(key=self.config.api.analytics_key)
        else:
            log.warning("No Dashbot API key configured, couldn't track")

    def init_cache(self) -> None:
        if self.config.redis_url:
            self.cache = Redis.from_url(self.config.redis_url, encoding="utf-8", decode_responses=True)
        else:
            log.warning("No Redis URL configured, using cache in local memory")
            self.cache = TTLOrderedDict()

    def close_cache(self) -> None:
        if self.cache is not None:
            self.cache.close()

    async def init_db(self) -> None:
        if self.config.database.url:
            db_url = self.config.database.url
        else:
            log.warning("No Database URL configured, using in-memory SQLite")
            db_url = "sqlite://:memory:"
        await Tortoise.init(db_url=db_url, modules={"models": ["bobotinho.models"]})
        await Tortoise.generate_schemas(safe=True)

    async def close_db(self) -> None:
        await Tortoise.close_connections()

    async def fetch_channels(self) -> None:
        await User.create(id=453651679, name="discretinho")  # NOTE: delete
        await Channel.create(user_id=453651679)  # NOTE: delete
        for channel in await Channel.all().select_related("user"):
            if channel.user.block:
                continue
            self.channels[channel.user.name] = {
                "id": channel.user_id,
                "banwords": list(channel.banwords.keys()),
                "disabled": list(channel.disabled.keys()),
                "online": channel.online,
            }

    async def fetch_users_block(self) -> None:
        self.ignore = await User.filter(block=True).all().values_list("id", flat=True)

    def add_global_checks(self) -> None:

        def is_online(ctx: Context) -> bool:
            if not self.channels[ctx.channel.name]["online"] and ctx.command.name != "start":
                raise exceptions.BotOffline
            return True

        def is_enable(ctx: Context) -> bool:
            if ctx.command.name in self.channels[ctx.channel.name]["disabled"]:
                raise exceptions.CommandDisabled
            return True

        self.check(is_online)
        self.check(is_enable)

    def load_modules(self) -> None:
        for filename in os.listdir(self.config.cogs_path):
            if filename.startswith("_") or not filename.endswith(".py"):
                continue
            try:
                cog = os.path.join(self.config.cogs_path, filename[:-3]).replace("/", ".")
                self.load_module(cog)
            except Exception as e:
                log.exception(e)

    async def start(self) -> None:
        self.init_analytics()
        self.init_cache()
        await self.init_db()
        await self.fetch_channels()
        await self.fetch_users_block()
        await self.connect()
        self.add_global_checks()
        self.load_modules()
        self.new_channels.start()
        self.check_channels.start()

    async def stop(self) -> None:
        self.new_channels.cancel()
        self.check_channels.cancel()
        self.close_cache()
        await self.close_db()
        await self.close()

    async def global_before_invoke(self, ctx: Context) -> None:
        log.info(f"#{ctx.channel.name} @{ctx.author.name}: {ctx.message.content}")
        if self.analytics:
            await self.analytics.received(
                author_id=ctx.author.id,
                author_name=ctx.author.name,
                channel_name=ctx.channel.name,
                message=ctx.message.content,
            )
        if not await User.exists(id=ctx.author.id):
            await User.create(
                id=ctx.author.id,
                channel=ctx.channel.name,
                name=ctx.author.name,
                color=ctx.author.colour,
                content=ctx.message.content.replace("ACTION", "", 1),
            )

    async def global_after_invoke(self, ctx: Context) -> None:
        if not ctx.response:
            return None
        try:
            await ctx.reply(f"@{ctx.author.name}, {ctx.response}")
        except Exception as e:
            log.exception(e, extra={"ctx": dict(ctx)})
        else:
            log.info(f"#{ctx.channel.name} @{self.nick}: {ctx.author.name}, {ctx.response}")
            if self.analytics:
                await self.analytics.sent(
                    author_id=ctx.author.id,
                    author_name=ctx.author.name,
                    channel_name=ctx.channel.name,
                    message=ctx.response,
                )

    async def event_ready(self) -> None:
        log.info(f"Prefix '{self.prefix}', {len(self.channels)} channels and {len(self.commands)} commands")

    async def event_command_error(self, ctx: Context, e: Exception) -> None:
        if isinstance(e, exceptions.BotOffline):
            log.warning(e)
        elif isinstance(e, exceptions.CommandDisabled):
            ctx.response = "esse comando está desativado nesse canal"
        elif isinstance(e, exceptions.MissingRequiredArgument):
            ctx.response = ctx.command.usage
        elif isinstance(e, exceptions.InappropriateMessage):
            ctx.response = "sua mensagem contém um termo banido"
        elif isinstance(e, exceptions.InvalidUsername):
            ctx.response = "nome de usuário inválido"
        elif isinstance(e, exceptions.AlreadyPlaying):
            ctx.response = "um jogo já está em andamento nesse canal"
        elif isinstance(e, exceptions.ModRequired):
            log.warning(e)
        elif isinstance(e, exceptions.PremiumRequired):
            log.warning(e)
        elif isinstance(e, exceptions.CommandOnCooldown):
            log.warning(e)
        elif isinstance(e, exceptions.CommandNotFound):
            pass
        else:
            ctx.response = "ocorreu um erro inesperado"
            log.error(e, extra={"ctx": dict(ctx)}, exc_info=e)

    async def event_message(self, message: Message) -> None:
        if message.echo:
            return None
        try:
            ctx = await self.get_context(message, cls=Context)
            await self.invoke(ctx)
        except exceptions.MissingRequiredArgument:
            await self.global_before_invoke(ctx)
            ctx.response = ctx.command.usage
            await self.global_after_invoke(ctx)
        except Exception as e:
            log.exception(e, extra={"ctx": dict(ctx)})
