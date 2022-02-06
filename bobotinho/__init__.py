# -*- coding: utf-8 -*-
from bobotinho.config import Config
from bobotinho.logger import Log

__title__ = "bobotinho-bot"
__author__ = "Leandro César"
__license__ = "GNU"
__copyright__ = "Copyright 2020 bobotinho"

log = Log(
    filename=Config.logger.filename,
    bugsnag={"key": Config.api.bugsnag_key, "version": Config.version, "stage": Config.stage},
)
