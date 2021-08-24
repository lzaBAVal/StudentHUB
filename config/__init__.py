from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

from config.db import DBConfig
from config.log import LogConfig
from config.redis import RedisConfig
from config.webhook import WebhookConfig


@dataclass
class Config:
    db: DBConfig
    redis: RedisConfig
    webhook: WebhookConfig
    app_dir: Path
    bot_token: str
    superusers: Iterable[int]
    log: LogConfig
    dump_chat_id: int


__all__ = [DBConfig, LogConfig, WebhookConfig, RedisConfig]
