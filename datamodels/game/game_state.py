from typing import Dict, List, Optional

from pydantic import BaseModel


class Bid(BaseModel):
    user_name: int
    value: int
    amount: int


class GameState(BaseModel):
    game_id: str
    user_mapping: Dict[str, int]
    user_mapping_reverse: Dict[int, str]
    bids_history: List[Bid]
    users_cubes_count: Dict[int, int]
    users_cubes: Optional[Dict[int, np.array[int]]]
    active_user: int
    is_maputa: bool
    has_maputa: Dict[int, bool]
    game_stated: bool