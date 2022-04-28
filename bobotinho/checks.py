# -*- coding: utf-8 -*-
from bobotinho.commands import Context, Chatter


def _get_chatter(ctx: Context, channel: str = None, author: str = None) -> Chatter:
    if channel is None:
        channel = ctx.channel.name
    if author is None:
        author = ctx.author.name
    return ctx.bot.get_channel(channel).get_chatter(author)


def _is_vip(chatter: Chatter) -> bool:
    return chatter.badges and chatter.badges.get("vip")


def bot_is_mod(ctx: Context) -> bool:
    return _get_chatter(ctx, author=ctx.bot.nick).is_mod


def bot_is_vip(ctx: Context) -> bool:
    return _is_vip(_get_chatter(ctx, author=ctx.bot.nick))


def bot_is_sub(ctx: Context) -> bool:
    return _get_chatter(ctx, author=ctx.bot.nick).is_subscriber


def bot_has_role(ctx: Context) -> bool:
    chatter = _get_chatter(ctx, author=ctx.bot.nick)
    return chatter.is_mod or _is_vip(chatter) or chatter.is_subscriber


def user_is_mod(ctx: Context) -> bool:
    return ctx.author.is_mod


def user_is_vip(ctx: Context) -> bool:
    return _is_vip(ctx.author)


def user_is_sub(ctx: Context) -> bool:
    return ctx.author.is_subscriber


def user_has_role(ctx: Context) -> bool:
    return ctx.author.is_mod or _is_vip(ctx.author) or ctx.author.is_subscriber
