from datamodels.game_action import GameAction
from bot.queue.action_queue import ActionQueue


class Worker():
    def __init__(self, queue: ActionQueue):
        self.is_running: bool = True
        self.queue: ActionQueue = queue

    async def run(self) -> None:
        while (self.is_running):
            action: GameAction | None = await self._get_action()
            if action is None:
                continue
            await self._process_action(action)

    async def _get_action(self) -> GameAction | None:
        if await self.queue.is_empty():
            return None
        return await self.queue.get()

    async def _process_action(self, action: GameAction) -> None:
        pass
