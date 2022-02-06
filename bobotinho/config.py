# -*- coding: utf-8 -*-
import os


class BotConfig:
    cogs_path = os.environ.get("COGS_PATH", "bobotinho/cogs")
    color = os.environ.get("COLOR", 0x9147FF)
    dev = os.environ.get("DEV_NICK")
    prefix = os.environ.get("PREFIX", "%")
    token = os.environ.get("ACCESS_TOKEN")
    secret = os.environ.get("CLIENT_SECRET")
    site_url = os.environ.get("SITE_URL")
    bugs_url = os.environ.get("WEBHOOK_BUGS_URL")
    suggestions_url = os.environ.get("WEBHOOK_SUGGESTIONS_URL")
    redis_url = os.environ.get("REDIS_URL")


class DatabaseConfig:
    url = os.environ.get("DATABASE_URL")


class LoggerConfig:
    level = os.environ.get("LOG_LEVEL", "INFO")
    format = os.environ.get("LOG_FORMAT")
    filename = os.environ.get("LOG_FILE_CONFIG", "logging_config.ini")


class APIsConfig:
    analytics_key = os.environ.get("DASHBOT_KEY")
    bugsnag_key = os.environ.get("BUGSNAG_KEY")
    currency_key = os.environ.get("COINAPI_KEY")
    weather_key = os.environ.get("OWM_KEY")
    wit_token = os.environ.get("WIT_TOKEN")


class Config(BotConfig):
    stage = os.environ.get("STAGE", "local")
    version = os.environ.get("VERSION")
    database = DatabaseConfig
    logger = LoggerConfig
    api = APIsConfig
