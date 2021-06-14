import os

from aiogram import types, Dispatcher, Bot
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from config.main import load_config
from models.config import Config
from utils.log.logging_core import Logger

logger = Logger(__name__)
current_config = load_config()

os.environ['STUDY_BOT_TOKEN'] = '1772267916:AAGgWfubaeStMlzPFYyrfJbJtinVxkZgxM4'
bot = Bot(current_config.bot_token, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot, storage=MemoryStorage())


def setup(config: Config):
    import filters
    from utils import executor
    from bot import middleware

    logger.debug(f"As application dir using: {config.app_dir}")

    filters.setup(dp, config)
    executor.setup(config)
    middleware.setup(dp, config)

    logger.info("Configure handlers...")
    import bot.handlers
