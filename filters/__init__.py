from functools import partialmethod

from aiogram import Dispatcher

from models.config import Config
from utils.log.logging_core import Logger

logger = Logger(__name__)


def setup(dispatcher: Dispatcher, config: Config):
    logger.info("Configure filters...")
    from .captain import CaptainFilter

    text_message = [
        dispatcher.message_handler(),
        dispatcher.edited_message_handler(),
        dispatcher.callback_query_handler()
    ]
    # CaptainFilter.check = partialmethod(CaptainFilter.check, config.superusers)

    dispatcher.filters_factory.bind(CaptainFilter)
