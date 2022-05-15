from bobotinho.config import Config
from bobotinho.logger import Log

config = Config()

__title__ = "bobotinho-bot"
__author__ = "Leandro César"
__license__ = "GNU"
__copyright__ = "Copyright 2020 bobotinho"
__version__ = config.version

log = Log(
    filename=config.log_filename,
    stage=config.stage,
    version=__version__,
    bugsnag_key=config.bugsnag_key,
    level=config.log_level,
)
