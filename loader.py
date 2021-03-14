import logging, asyncio

from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram import Bot, Dispatcher
from DB.pgsql import Database
from schedule.harvest.harvest_main import Harvest, scheduler
from config import token
from logging_core import init_logger

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


async def on_startup(x):
    asyncio.create_task(scheduler(db))

async def on_shutdown(x):
    logger.info('Bot has stopped')