from typing import Optional, Union

from pydantic import BaseModel
from enum import StrEnum
from datamodels.game.game_state import Bid


class CreateGameAction(BaseModel):
    type: str = "create_game"
    game_id: str


class ConnectGameAction(BaseModel):
    type: str = "connect_game"
    game_id: str


class DisconnectGameAction(BaseModel):
    type: str = "disconnect_game"


class StartGameAction(BaseModel):
    type: str = "start_game"


class RaseAction(BaseModel):
    type: str = "rase"
    bid: Bid


class CheckAction(BaseModel):
    type: str = "check"


class CheckEqualAction(BaseModel):
    type: str = "check_equal"


class AskHistoryAction(BaseModel):
    type: str = "ask_history"


InputGameAction = CreateGameAction | ConnectGameAction | DisconnectGameAction | StartGameAction | RaseAction | CheckAction | CheckEqualAction | AskHistoryAction


class GameAction(BaseModel):
    user_id: str
    action: InputGameAction
    game_id: str
