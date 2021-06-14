import os

from models.config.db import DBConfig


def load_db_config():
    db_config = DBConfig()
    db_config.db_type = os.getenv("DB_TYPE", default='postgres')
    db_config.login = os.getenv("DB_LOGIN", "samplerole")
    db_config.password = os.getenv("DB_PASSWORD", "Cyberark!123")
    db_config.db_name = os.getenv("DB_NAME", "testDB")
    db_config.db_host = os.getenv("DB_HOST", default='localhost')
    port = os.getenv("DB_PORT")
    if port is None:
        if db_config.db_type == 'mysql':
            db_config.db_port = 3306
        elif db_config.db_type == 'postgres':
            db_config.db_port = 5432
    else:
        db_config.db_port = int(port)
    db_config.db_path = os.getenv("DB_PATH", "")
    return db_config
