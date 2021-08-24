import os
import secrets
from dataclasses import dataclass


@dataclass
class WebhookConfig:
    host: str
    port: int
    path: str
    listen_host: str = 'localhost'
    listen_port: int = 3000
    secret_str: str = secrets.token_urlsafe(16)

    @property
    def url_base(self) -> str:
        return f"https://{self.host}:{self.port}{self.path}"

    @property
    def external_url(self) -> str:
        return f"{self.url_base}{self.secret_str}/"

    @property
    def listener_kwargs(self) -> dict:
        return dict(
            host=self.listen_host,
            port=self.listen_port,
            webhook_path=f"/{self.secret_str}/",
        )


def load_webhook_config() -> WebhookConfig:
    return WebhookConfig(
        host=os.getenv("WEBHOOK_HOST"),
        port=os.getenv("WEBHOOK_PORT", default=8443),
        path=os.getenv("WEBHOOK_PATH", default='/'),
        listen_host=os.getenv("LISTEN_IP", default='192.168.1.163'),
        listen_port=os.getenv("LISTEN_PORT", default=8443),
    )
