# -*- coding: utf-8 -*-
import os


class BotConfig:
    """Bot configuration variables"""

    color = os.environ.get("COLOR", 0x9147FF)
    dev = os.environ.get("DEV")
    prefix = os.environ.get("PREFIX", "%")
    token = os.environ.get("ACCESS_TOKEN")
    secret = os.environ.get("CLIENT_SECRET")
    site_url = os.environ.get("SITE_URL")
    bugs_url = os.environ.get("WEBHOOK_BUGS_URL")
    suggestions_url = os.environ.get("WEBHOOK_SUGGESTIONS_URL")
    redis_url = os.environ.get("REDIS_URL")


class DatabaseConfig:
    """Database configuration variables"""

    user = os.environ.get("DB_USER")
    password = os.environ.get("DB_PASSWORD")
    host = os.environ.get("DB_HOST")
    name = os.environ.get("DB_NAME")
    url = os.environ.get("DB_URL", "sqlite://:memory:")


class LoggerConfig:
    """Logging configuration variables"""

    level = os.environ.get("LOG_LEVEL", "INFO")
    format = os.environ.get("LOG_FORMAT")
    filename = os.environ.get("LOG_FILE_CONFIG")


class APIsConfig:
    """APIs configuration variables"""

    bugsnag_key = os.environ.get("BUGSNAG_KEY")
    currency_key = os.environ.get("COINAPI_KEY")
    analytics_key = os.environ.get("DASHBOT_KEY")
    own_key = os.environ.get("OWM_KEY")


class Config(BotConfig):
    """All configuration variables"""

    stage = os.environ.get("STAGE", "local")
    version = os.environ.get("VERSION")
    database = DatabaseConfig
    logger = LoggerConfig
    api = APIsConfig
