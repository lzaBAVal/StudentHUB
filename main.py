from loader import bot, dp, on_shutdown, on_startup
from logs.logging_core import init_logger


if __name__ == '__main__':
    logger = init_logger()

    bot = bot
    dp = dp

    from aiogram import executor
    from bot.handlers import dp

    logger.debug('Bot started')
    executor.start_polling(dp, skip_updates=False, on_startup=on_startup, on_shutdown=on_shutdown)
    # executor.start_polling(dp, skip_updates=False, on_shutdown=loader.on_shutdown)
