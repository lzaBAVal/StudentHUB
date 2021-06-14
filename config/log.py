from pathlib import Path

from models.config.log import LogConfig


def load_log_config(app_dir: Path) -> LogConfig:
    return LogConfig(
        log_chat_id=690976128,
        log_path=app_dir / "log",
    )