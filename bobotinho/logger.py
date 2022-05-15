# -*- coding: utf-8 -*-
import logging
import logging.config
from logging import Logger

import bugsnag
from bugsnag.handlers import BugsnagHandler


class Log(Logger):
    def __new__(cls, *, filename: str = None, stage: str = None, version: str = None, bugsnag_key: str = None, **kwargs) -> Logger:
        if filename:
            cls.config_from_file(filename)
        else:
            cls.config_from_args(**kwargs)
        logger = logging.getLogger()
        cls.inject_bugsnag_handler(logger, key=bugsnag_key, stage=stage, version=version)
        return logger

    @staticmethod
    def config_from_file(filename: str) -> None:
        logging.config.fileConfig(filename)

    @staticmethod
    def config_from_args(**kwargs) -> None:
        logging.basicConfig(**kwargs)

    @staticmethod
    def inject_bugsnag_handler(logger: Logger, *, key: str = None, stage: str = None, version: str = None) -> None:
        if key:
            bugsnag.configure(app_version=version, api_key=key, release_stage=stage)
            extra_fields = {"log": ["__repr__"], "locals": ["locals"], "ctx": ["ctx"]}
            bugsnag_handler = BugsnagHandler(extra_fields=extra_fields)
            bugsnag_handler.setLevel(logging.ERROR)
            logger.addHandler(bugsnag_handler)
        else:
            logger.warning("No Bugsnag API key configured, couldn't notify")
