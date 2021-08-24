from aiogram import Dispatcher

from config import Config
from log.logging_core import init_logger

# logger = Logger(__name__)
logger = init_logger()

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
