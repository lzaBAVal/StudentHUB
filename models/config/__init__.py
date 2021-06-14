from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


from .db import DBConfig
from .log import LogConfig
from .tg_client import TgClientConfig
from .webhook import WebhookConfig


@dataclass
class Config:
    db: DBConfig
    webhook: WebhookConfig
    app_dir: Path
    bot_token: str
    superusers: Iterable[int]
    log: LogConfig
    dump_chat_id: int
    tg_client: TgClientConfig


__all__ = [DBConfig, LogConfig, WebhookConfig, TgClientConfig]
