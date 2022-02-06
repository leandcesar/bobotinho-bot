# -*- coding: utf-8 -*-
from twitchio.ext.commands.errors import (  # NOQA
    BadArgument,
    CheckFailure,
    CommandNotFound,
    CommandOnCooldown,
    MissingRequiredArgument,
)


class InvalidUsername(BadArgument):
    """Invalid username."""


class AlreadyPlaying(CheckFailure):
    """A game is already running on channel."""


class BotOffline(CheckFailure):
    """Bot is offline on channel."""


class CommandDisabled(CheckFailure):
    """Command is disabled on channel."""


class InappropriateMessage(CheckFailure):
    """Message has an inappropiate content on channel."""


class ModRequired(CheckFailure):
    """User is not allowed to use the command on channel."""


class PremiumRequired(CheckFailure):
    """User is not allowed to use the command on channel."""
