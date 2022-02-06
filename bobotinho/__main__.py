# -*- coding: utf-8 -*-
from bobotinho import log
from bobotinho.bot import Bot
from bobotinho.config import Config


if __name__ == "__main__":
    try:
        bot = Bot(config=Config)
        bot.loop.create_task(bot.start())
        bot.loop.run_forever()
    except KeyboardInterrupt:
        pass
    except BaseException as e:
        log.exception(e, extra={"locals": locals()})
    finally:
        bot.loop.run_until_complete(bot.stop())
        bot.loop.close()
