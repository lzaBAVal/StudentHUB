import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from DB.pgsql import Database
from bot.middleware.ratelimit import ThrottlingMiddleware
from config import token
from logs.logging_core import init_logger
from schedule_json.harvest.harvest_main import Harvest, scheduler

API_TOKEN = token

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = init_logger()

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
loop = asyncio.get_event_loop()
db = Database(loop)
hrvst = Harvest(db)
dp.middleware.setup(ThrottlingMiddleware())


# dp.middleware.setup(CheckStateMiddleware())

async def on_startup(x):
    asyncio.create_task(scheduler(db))


async def on_shutdown(x):
    logger.info('Bot has stopped')
