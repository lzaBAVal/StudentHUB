from aiogram import Dispatcher

from bot.middleware.ratelimit import CheckStateMiddleware, ThrottlingMiddleware, CheckBannedUser, \
    CheckCaptainMiddleware, CountClick, HandlerCounter
from config import Config
from log.logging_core import init_logger

# logger = Logger(__name__)
logger = init_logger()


def setup(dispatcher: Dispatcher, config: Config):
    logger.info("Configure middlewares...")
    dispatcher.middleware.setup(CheckBannedUser())
    dispatcher.middleware.setup(ThrottlingMiddleware())
    dispatcher.middleware.setup(CheckStateMiddleware())
    dispatcher.middleware.setup(CheckCaptainMiddleware())
    dispatcher.middleware.setup(CountClick())
    dispatcher.middleware.setup(HandlerCounter())
