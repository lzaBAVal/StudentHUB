from loader import dp, on_shutdown, on_startup
from utils.log.logging_core import init_logger
import bot.handlers

if __name__ == '__main__':
    logger = init_logger()

    bot = bot
    dp = dp

    from aiogram import executor

    logger.debug('Bot started')

    import bot.handlers

    executor.start_polling(dp, skip_updates=False, on_startup=on_startup, on_shutdown=on_shutdown)
