import os
from functools import lru_cache
from pathlib import Path

from config import Config
from config.db import load_db_config
from config.log import load_log_config
from config.redis import load_redis_config
from config.webhook import load_webhook_config


@lru_cache
def load_config() -> Config:
    app_dir: Path = Path(__file__).parent.parent

    _bot_token = os.getenv("STUDY_BOT_TOKEN", default='1853354220:AAFmOW-SxmhZ16P-FKq2phjIJ7uGvUB97wY')
    _super_user = os.getenv("SUPERUSER", default=['690976128', '354203111'])

    return Config(
        db=load_db_config(),
        redis=load_redis_config(),
        webhook=load_webhook_config(),
        app_dir=app_dir,
        bot_token=_bot_token,
        superusers=_super_user,
        log=load_log_config(app_dir=app_dir, log_chat_id=_super_user),
        dump_chat_id=_super_user,
    )