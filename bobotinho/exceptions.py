# -*- coding: utf-8 -*-


class BobotinhoException(Exception):
    """Base exception class for Bobotinho."""


class CheckFailed(BobotinhoException):
    """A command check failed occurred."""


class DatabaseException(BobotinhoException):
    """A database operation exception occurred."""


class InvalidArgument(BobotinhoException):
    """An invalid argument has been passed."""


class RequestException(BobotinhoException):
    """An HTTP exception occurred."""


class BotOffline(CheckFailed):
    """Bobotinho is offline on channel."""


class InappropriateMessage(CheckFailed):
    """Content message has a inappropiate word on channel"""


class CommandDisabled(CheckFailed):
    """Command is disabled on channel."""


class UserNotAllowed(CheckFailed):
    """User is not allowed to send link on channel."""


class AlreadyPlaying(CheckFailed):
    """One game is already running on channel."""


class InvalidChannel(InvalidArgument):
    """An invalid channel name was passed."""


class InvalidUser(InvalidArgument):
    """An invalid user name was passed."""


class IntegrationException(RequestException):
    """An HTTP exception occurred in API integration."""


class WebhookException(RequestException):
    """An HTTP exception occurred in webhooks."""
