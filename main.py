import asyncio
import os
import yaml

from bot.puller.puller import Puller
from bot.queue.action_queue import ActionQueue
from bot.worker.worker import Worker
from datamodels.bot_config import BotConfig


async def main():
    config = BotConfig(**yaml.load(open('configs/bot_config.yaml'), Loader=yaml.BaseLoader))
    tg_token: str | None = os.environ.get(config.tg_token_env_name)
    if tg_token is None:
        raise ValueError(f'No tg token in {config.tg_token_env_name}')
    queue = ActionQueue()
    puller = asyncio.create_task(Puller(queue, tg_token).run())
    workers = [
        asyncio.create_task(Worker(queue).run()) for _ in range(config.num_workers)
    ]
    asyncio.gather(puller, *workers)


if __name__ == '__main__':
    asyncio.run(main())
