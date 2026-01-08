from enum import StrEnum
from typing import Optional, Union

from pydantic import BaseModel


class CreateGameAction(BaseModel):
    type: str = "create_game"
    game_id: str


# class CreateGameAction(BaseModel):
#     type: str = "create_game"


# class ConnectGameAction(BaseModel):
#     type: str = "connect_game"
#     game_id: str


# class DisconnectGameAction(BaseModel):
#     type: str = "disconnect_game"


# class StartGameAction(BaseModel):
#     type: str = "start_game"


# class RaseAction(BaseModel):
#     type: str = "rase"
#     cubes_value: Optional[int]
#     cubes_amount: Optional[int]


# class CheckAction(BaseModel):
#     type: str = "check"


# class CheckEqualAction(BaseModel):
#     type: str = "check_equal"


# class AskHistoryAction(BaseModel):
#     type: str = "ask_history"


# InputGameAction = CreateGameAction | ConnectGameAction | DisconnectGameAction | StartGameAction | RaseAction | CheckAction | CheckEqualAction | AskHistoryAction


class GameAction(BaseModel):
    chat_id: int
    action: UserCommands | UserMessage
