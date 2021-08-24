import os

import prometheus_client
from aiogram import types, Dispatcher, Bot
from aiogram.contrib.fsm_storage.redis import RedisStorage

from config import Config
from config.main import load_config
from log.logging_core import init_logger

logger = init_logger()
current_config = load_config()

bot = Bot(current_config.bot_token, parse_mode=types.ParseMode.HTML)
redis_host = os.getenv("REDIS_HOST", default='192.168.35.153')
redis_port = os.getenv("REDIS_PORT", default='6379')
redis_db = os.getenv("REDIS_DB", default=1)
storage = RedisStorage(redis_host, redis_port, db=redis_db)

dp = Dispatcher(bot, storage=storage)


def setup(config: Config):
    from bot import filters
    from bot import middleware
    from utils import executor

    logger.debug(f"As application dir using: {config.app_dir}")

    filters.setup(dp, config)
    executor.setup(config)
    middleware.setup(dp, config)

    logger.info("Configure handlers...")
    import bot.handlers

    logger.info("Configure prometheus_client server...")
    prometheus_client.start_http_server(8000)
