import loader
from logs.logging_core import init_logger
# ----------------------------------------------------------------------------------------------------


if __name__ == '__main__':
    bot = loader.bot
    dp = loader.dp
    logger = init_logger()


    from aiogram import executor
    from bot.handlers import dp

    logger.debug('Bot started')
    executor.start_polling(dp, skip_updates=False, on_startup=loader.on_startup, on_shutdown=loader.on_shutdown)
    #executor.start_polling(dp, skip_updates=False, on_shutdown=loader.on_shutdown)

