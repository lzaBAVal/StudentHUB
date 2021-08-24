import os
from dataclasses import dataclass

from log.logging_core import init_logger

# logger = Logger(__name__)
logger = init_logger()

@dataclass
class RedisConfig:
    redis_host: str = None
    redis_port: str = None
    redis_db: str = None


def load_redis_config() -> RedisConfig:
    redis_config = RedisConfig()
    redis_config.redis_host = os.getenv("REDIS_HOST", default='192.168.35.153')
    redis_config.redis_port = os.getenv("REDIS_PORT", default='6379')
    redis_config.redis_db = os.getenv("REDIS_DB", default='1')
    return redis_config
