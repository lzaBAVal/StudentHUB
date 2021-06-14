from functools import partial

from aiogram import Dispatcher
from aiogram.utils.executor import Executor
from tortoise import Tortoise

import models

from models.config.db import DBConfig
from utils.log.logging_core import Logger

logger = Logger(__name__)


async def on_startup(_: Dispatcher, db_config: DBConfig):
    await db_init(db_config)


async def db_init(db_config: DBConfig):
    db_url = db_config.create_url_config()
    print(db_url)
    logger.info(f"connecting to db {db_url}", db_url=db_url)
    await Tortoise.init(
        db_url=db_url,
        modules={'models': [models]}
    )


async def on_shutdown(_: Dispatcher):
    await Tortoise.close_connections()


def setup(executor: Executor, db_config: DBConfig):
    executor.on_startup(partial(on_startup, db_config=db_config))
    executor.on_shutdown(on_shutdown)