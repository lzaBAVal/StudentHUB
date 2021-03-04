import logging, aiogram, asyncio, asyncpg

from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram import Bot, Dispatcher, executor, types
from DB.pgsql import Database

API_TOKEN = '1533907938:AAFdL_sf1pH_FwNZqxihjX7JqDUcOk5bXKE'

# Configure logging
logging.basicConfig(level=logging.INFO)


# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
loop = asyncio.get_event_loop()
db = Database(loop)
