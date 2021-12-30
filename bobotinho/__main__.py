# -*- coding: utf-8 -*-
import sys

from bobotinho import config, log

try:
    from bobotinho.database import Database

    db: Database = Database(config.database_url)
except Exception as e:
    log.critical(e, exc_info=1)
    sys.exit("[CRITICAL] Database constructor failure")

try:
    from bobotinho.bots import TwitchBot

    bot: TwitchBot = TwitchBot(config)
    bot.load_cogs()
except Exception as e:
    log.critical(e, exc_info=1)
    sys.exit("[CRITICAL] Twitch Bot constructor failure")

try:
    from redis import Redis

    bot.cache = Redis.from_url(config.redis_url, encoding="utf-8", decode_responses=True)
except Exception as e:
    from bobotinho.cache import TTLOrderedDict

    log.warning(e)
    bot.cache = TTLOrderedDict()

if __name__ == "__main__":
    try:
        bot.loop.run_until_complete(db.init())
        bot.loop.run_until_complete(bot.start())
        bot.loop.run_forever()
    except BaseException as e:
        log.exception(e, extra={"locals": locals()})
        bot.loop.run_until_complete(db.close(e))
    else:
        bot.loop.run_until_complete(db.close())
    finally:
        bot.cache.close()
        bot.loop.run_until_complete(bot.stop())
        bot.loop.close()