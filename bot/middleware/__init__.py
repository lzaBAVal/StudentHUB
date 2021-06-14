from aiogram import Dispatcher

from bot.middleware.ratelimit import CheckStateMiddleware, ThrottlingMiddleware, CheckBannedUser, CheckCaptainMiddleware
from models.config import Config
from utils.log.logging_core import Logger

logger = Logger(__name__)


def setup(dispatcher: Dispatcher, config: Config):
    logger.info("Configure middlewares...")
    dispatcher.middleware.setup(CheckBannedUser())
    dispatcher.middleware.setup(ThrottlingMiddleware())
    dispatcher.middleware.setup(CheckStateMiddleware())
    dispatcher.middleware.setup(CheckCaptainMiddleware())
