from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command

from bot.queue.action_queue import ActionQueue
from datamodels.game_action import *


dp: Dispatcher = Dispatcher()

class Puller(object):
    def __init__(self, queue: ActionQueue, tg_token: str):
        self.queue: ActionQueue = queue
        self.tg_token: str = tg_token
        self.bot: Bot = Bot(token=self.tg_token)

    @dp.message(Command("/start"))
    async def say_hello(self, message: types.Message):
        await self.bot.send_message(chat_id=message.chat.id, text="Hello in the best perudo bot ever!")
    
    @dp.message(Command())
    async def create_game(self, message: types.Message):
        try:
            user_command: UserCommands = UserCommands(message.text)
        except ValueError:
            await self.bot.send_message(chat_id=message.chat.id, text="Invalid command")
            return
        await self.queue.put(
            GameAction(
                chat_id=message.chat.id,
                action=UserCommands(user_command)
            )
        )

    @dp.message()
    async def default(self, message: types.Message):
        await self.queue.put(
            GameAction(
                chat_id=message.chat.id,
                action=UserMessage(text=message.text)
            )
        )

    async def run(self):
        await dp.start_polling(self.bot)
