import asyncio

from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.redis import RedisStorage2
from aiogram.dispatcher import DEFAULT_RATE_LIMIT
from aiogram.dispatcher.handler import CancelHandler, current_handler
from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram.utils.exceptions import Throttled

TOKEN = 'BOT_TOKEN_HERE'

# In this example Redis storage is used
storage = RedisStorage2(db=5)

bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=storage)





@dp.message_handler(commands=['start'])
@rate_limit(5, 'start')  # this is not required but you can configure throttling manager for current handler using it
async def cmd_test(message: types.Message):
    # You can use this command every 5 seconds
    await message.reply('Test passed! You can use this command every 5 seconds.')


if __name__ == '__main__':
    # Setup middleware
    dp.middleware.setup(ThrottlingMiddleware())

    # Start long-polling
    executor.start_polling(dp)