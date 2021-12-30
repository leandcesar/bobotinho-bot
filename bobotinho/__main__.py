# -*- coding: utf-8 -*-
import sys
from redis import Redis

from bobotinho import config, database, log
from bobotinho.bot import TwitchBot
from bobotinho.cache import TTLOrderedDict


if __name__ == "__main__":
    try:
        bot = TwitchBot(config)
        bot.load_cogs()
    except Exception as e:
        log.critical(e, exc_info=1)
        sys.exit("[CRITICAL] Twitch Bot constructor failure")
    try:
        bot.cache = Redis.from_url(config.redis_url, encoding="utf-8", decode_responses=True)
    except Exception as e:
        log.warning(e)
        bot.cache = TTLOrderedDict()
    try:
        bot.loop.run_until_complete(database.init(config.database.url))
        bot.loop.run_until_complete(bot.start())
        bot.loop.run_forever()
    except BaseException as e:
        log.exception(e, extra={"locals": locals()})
    finally:
        bot.cache.close()
        bot.loop.run_until_complete(database.close())
        bot.loop.run_until_complete(bot.stop())
        bot.loop.close()
