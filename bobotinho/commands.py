# -*- coding: utf-8 -*-
from typing import Callable

from twitchio.ext.commands import *
from twitchio.ext.routines import *
from twitchio.message import *


class CommandPlus(Command):
    def __init__(self, name: str, func: Callable, description: str = None, usage: str = None, **attrs) -> None:
        super().__init__(name, func, **attrs)
        try:
            self.description = func.__description__
        except AttributeError:
            self.description = description
        try:
            self.usage = func.__usage__
        except AttributeError:
            self.usage = usage


def command(
    *, name: str = None, description: str = None, usage: str = None, aliases: Union[list, tuple] = None, no_global_checks=False
) -> Callable[[Callable], CommandPlus]:

    def decorator(func: Callable) -> CommandPlus:
        fname = name or func.__name__
        return CommandPlus(
            name=fname,
            func=func,
            description=description,
            usage=usage,
            aliases=aliases,
            no_global_checks=no_global_checks,
        )

    return decorator


def check(func: Callable) -> Callable[[Callable], CommandPlus]:

    def decorator(command: CommandPlus) -> CommandPlus:
        command._checks.append(func)
        return command

    return decorator


def helper(*, description: str, usage: str = None) -> Callable[[Callable], CommandPlus]:

    def decorator(command: CommandPlus) -> CommandPlus:
        if isinstance(command, Command):
            command.description = description
            command.usage = usage
        else:
            command.__description__ = description
            command.__usage__ = usage
        return command

    return decorator


class Checks:
    @staticmethod
    def _get_chatter(ctx: Context, channel: str = None, author: str = None) -> Chatter:
        if channel is None:
            channel = ctx.channel.name
        if author is None:
            author = ctx.author.name
        return ctx.bot.get_channel(channel).get_chatter(author)

    @staticmethod
    def _is_vip(chatter: Chatter) -> bool:
        return chatter.badges and chatter.badges.get("vip")

    @staticmethod
    def bot_is_mod(ctx: Context) -> bool:
        return _get_chatter(ctx, author=ctx.bot.nick).is_mod

    @staticmethod
    def bot_is_vip(ctx: Context) -> bool:
        return _is_vip(_get_chatter(ctx, author=ctx.bot.nick))

    @staticmethod
    def bot_is_sub(ctx: Context) -> bool:
        return _get_chatter(ctx, author=ctx.bot.nick).is_subscriber

    @staticmethod
    def bot_has_role(ctx: Context) -> bool:
        chatter = _get_chatter(ctx, author=ctx.bot.nick)
        return chatter.is_mod or _is_vip(chatter) or chatter.is_subscriber

    @staticmethod
    def user_is_mod(ctx: Context) -> bool:
        return ctx.author.is_mod

    @staticmethod
    def user_is_vip(ctx: Context) -> bool:
        return _is_vip(ctx.author)

    @staticmethod
    def user_is_sub(ctx: Context) -> bool:
        return ctx.author.is_subscriber

    @staticmethod
    def user_has_role(ctx: Context) -> bool:
        return ctx.author.is_mod or _is_vip(ctx.author) or ctx.author.is_subscriber
