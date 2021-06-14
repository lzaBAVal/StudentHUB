import os

import yaml
from dotenv import load_dotenv

from functools import lru_cache
from pathlib import Path

from config.db import load_db_config

from config.log import load_log_config
from config.webhook import load_webhook_config
from models.config import Config
from models.config.tg_client import TgClientConfig


@lru_cache
def load_config() -> Config:
    app_dir: Path = Path(__file__).parent.parent
    load_dotenv(str(app_dir / '.env'))

    #_bot_token = os.getenv("STUDY_BOT_TOKEN")
    _bot_token = '1772267916:AAGgWfubaeStMlzPFYyrfJbJtinVxkZgxM4'
    with (app_dir / 'config' / "bot_config.yml").open('r', encoding="utf-8") as f:
        config_file_data = yaml.load(f, Loader=yaml.FullLoader)

    return Config(
        db=load_db_config(),
        webhook=load_webhook_config(),
        app_dir=app_dir,
        bot_token=_bot_token,
        superusers=frozenset(config_file_data['superusers']),
        log=load_log_config(app_dir=app_dir),
        dump_chat_id=690976128,  # ⚙️Testing Area >>> Python Scripts,
        tg_client=TgClientConfig(bot_token=_bot_token)
    )