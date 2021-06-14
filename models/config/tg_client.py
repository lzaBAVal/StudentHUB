from dataclasses import dataclass


@dataclass
class TgClientConfig:
    bot_token: str
    #api_hash: str
    #api_id: int