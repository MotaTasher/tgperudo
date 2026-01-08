from pydantic import BaseModel


class BotConfig(BaseModel):
    num_workers: int
    tg_token_env_name: str
