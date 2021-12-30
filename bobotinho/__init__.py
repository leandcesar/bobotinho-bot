# -*- coding: utf-8 -*-
from bobotinho.config import Config
from bobotinho.logger import Log

__title__ = "bobotinho-bot"
__author__ = "Leandro César"
__license__ = "GNU"
__copyright__ = "Copyright 2020 bobotinho"
__version__ = Config.version

config = Config
log = Log(
    filename=config.logger.filename,
    bugsnag={"key": config.api.bugsnag_key, "version": config.version, "stage": config.stage},
)
