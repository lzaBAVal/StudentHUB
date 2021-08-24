from contextlib import suppress
from functools import partial

from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.utils.exceptions import TelegramAPIError
from aiogram.utils.executor import Executor

from DB.models.db import db
from bot.keyboard.keyboard import stud_kb
from config import Config
from config import WebhookConfig
from log.logging_core import init_logger
from misc import dp

# logger = Logger(__name__)
logger = init_logger()
runner = Executor(dp)


async def on_startup_webhook(dispatcher: Dispatcher, webhook_config: WebhookConfig):
    webhook_url = webhook_config.external_url
    logger.info("Configure Web-Hook URL to: {url}", url=webhook_url)
    await dispatcher.bot.set_webhook(webhook_url)


# Notify log chat id
async def on_startup_notify(dispatcher: Dispatcher, config: Config):
    with suppress(TelegramAPIError):
        await dispatcher.bot.send_message(chat_id=config.log.log_chat_id,
                                          text="Bot started",
                                          disable_notification=True)
        logger.info("Notified about bot is started.")


def setup(config: Config):
    logger.info("Configure executor...")
    db.setup(runner, config.db)
    # partial add new arguments in runner
    runner.on_startup(partial(on_startup_webhook, webhook_config=config.webhook), webhook=True, polling=False)
    runner.on_startup(partial(on_startup_notify, config=config))
