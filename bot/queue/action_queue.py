from asyncio import Queue

from datamodels.game_action import GameAction


class ActionQueue(object):
    def __init__(self):
        self.queue: Queue[GameAction] = Queue()
    
    async def is_empty(self) -> bool:
        return self.queue.empty()
    
    async def put(self, item: GameAction):
        await self.queue.put(item)
    
    async def get(self) -> GameAction:
        return await self.queue.get()
    

