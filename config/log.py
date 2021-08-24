from dataclasses import dataclass
from pathlib import Path


@dataclass
class LogConfig:
    log_chat_id: int
    log_path: Path
    filename: str = "print.log"

    @property
    def log_file(self):
        return self.log_path / self.filename


def load_log_config(app_dir: Path, log_chat_id: int) -> LogConfig:
    return LogConfig(
        log_chat_id=log_chat_id,
        log_path=app_dir / "log",
    )