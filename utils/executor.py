from contextlib import suppress
from functools import partial

from aiogram import Dispatcher
from aiogram.utils.exceptions import TelegramAPIError
from aiogram.utils.executor import Executor

from bot.keyboard.keyboard import stud_kb
from misc import dp
from models.config import Config
from models.config.webhook import WebhookConfig
from models.db import db

from utils.log.logging_core import Logger

logger = Logger(__name__)
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
                                          disable_notification=True, reply_markup=stud_kb())
        logger.info("Notified about bot is started.")


def setup(config: Config):
    logger.info("Configure executor...")
    db.setup(runner, config.db)
    # partial add new arguments in runner
    runner.on_startup(partial(on_startup_webhook, webhook_config=config.webhook), webhook=True, polling=False)
    runner.on_startup(partial(on_startup_notify, config=config))