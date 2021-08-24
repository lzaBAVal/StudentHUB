import os
from dataclasses import dataclass

from log.logging_core import init_logger

# logger = Logger(__name__)
logger = init_logger()

@dataclass
class DBConfig:
    db_type: str = None
    login: str = None
    password: str = None
    db_name: str = None
    db_host: str = None
    db_port: int = None
    db_path: str = None

    def create_url_config(self):
        if self.db_type == 'mysql':
            db_url = (
                f'{self.db_type}://{self.login}:{self.password}'
                f'@{self.db_host}:{self.db_port}/{self.db_name}'
            )
        elif self.db_type == 'postgres':
            db_url = (
                f'{self.db_type}://{self.login}:{self.password}'
                f'@{self.db_host}:{self.db_port}/{self.db_name}'
            )
        elif self.db_type == 'sqlite':
            db_url = (
                f'{self.db_type}://{self.db_path}'
            )
        else:
            raise ValueError("DB_TYPE not mysql, sqlite or postgres")
        logger.debug(db_url)
        return db_url


def load_db_config() -> DBConfig:
    db_config = DBConfig()
    db_config.db_type = os.getenv("DB_TYPE", default='postgres')
    db_config.login = os.getenv("DB_LOGIN", "postgres")
    db_config.password = os.getenv("DB_PASSWORD", "postgres")
    db_config.db_name = os.getenv("DB_NAME", ""
                                             "")
    db_config.db_host = os.getenv("DB_HOST", default='23.105.226.171')
    db_config.db_port = os.getenv("DB_PORT", default=5432)
    db_config.db_path = os.getenv("DB_PATH", "")
    return db_config
