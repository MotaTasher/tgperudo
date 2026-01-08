from datamodels.game_action import GameAction
from bot.queue.action_queue import ActionQueue

from datamodels.game.game_state import GameState, Bid
from typing import Dict, List
import asyncio
from random import randint
import numpy as np

class GameStateHolder():
    def __init__(self):
        self._dict: Dict[str, GameState] = dict()
        self._lock = asyncio.Lock()

    async def create(self, game_id) -> GameState | None:
        async with self._lock:
            if game_id in self._dict:
                return None

            self._dict[game_id] = GameState()
            self._dict[game_id].game_id = game_id
            return self._dict[game_id]

    def get(self, game_id) -> GameState | None:
        return self._dict.get(game_id, None)

    def pop(self, game_id) -> None:
        self._dict.pop(game_id, None)


USER_TO_GAME: Dict[str, GamteState] = dict()
GAMES_STATES: GameStateHolder = GameStateHolder()
JOKER_VALUE = 1


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
        user_id, message = self.queue.get()
        user_state = ...[user_id]
        state = user_state.update(message)
        if state:
            if await self.queue.is_empty():
                return None
            return await self.queue.get()

    async def _process_action(self, action: GameAction) -> None:
        if action.action.type == "create_game":
            game_id = action.action.game_id
            game = await GAMES_STATES.create(game_id)
            if game:
                game.user_mapping[action.user_id] = 0
                game.user_mapping_reverse[0] = action.user_id
            else:
                self._post_message(f"Game with id = \"{game_id}\" already exist", action.user_id)

        elif action.action.type == "connect_game":
            game = self._get_game(action.action.game_id, action.user_id)
            if game:
                USER_TO_GAME[action.user_id] = game
                game.user_mapping[action.user_id] = min(game.user_mapping.keys()) + 1
                game.user_mapping_reverse[game.user_mapping[action.user_id]] = action.user_id

        elif action.action.type == "disconnect_game":
            if game := self._get_game(action.action.game_id, action.user_id):
                self._remove_user(game, game.user_mapping[action.user_id])

        elif action.action.type == "start_game":
            if game := self._get_game(action.action.game_id, action.user_id):
                if min(game.user_mapping.keys()) == action.user_id:
                    self._generate_cubes_in_game(game)
                else:
                    self._post_message("You aren't game host (\"sad emoje\")")

        elif action.action.type == "rase":
            if game := self._get_game(action.action.game_id, action.user_id):
                if game.active_user == game.user_mapping[action.user_id]:
                    game.active_user = self._get_next_user(game)

                    # todo: check bid is leagal
                    game.bids_history.append(action.action.bid)
                else:
                    self._post_message("It's not your turn now")

        elif action.action.type == "check":
            if game := self._get_game(action.action.game_id, action.user_id):
                if game.active_user == game.user_mapping[action.user_id]:
                    if len(game.bids_history) == 0:
                        self._post_message("It's the first move now, you can't check")
                        return
                    last_bid = game.bids_history[-1]
                    amount = self._get_cubes_amount(game, last_bid)
                    if amount >= last_bid.amount:
                        loser_name = game.user_mapping[action.user_id]
                    else:
                        loser_name = self._get_prev_user(game)
                    game.users_cubes_count[loser_name] -= 1
                    if game.users_cubes_count[loser_name] == 0:
                        self._remove_user(loser_name)
                    self._show_game_info(game)
                    self._generate_cubes_in_game(game)
                    self._maputa_handler(game, loser_name)
                else:
                    self._post_message("It's not your turn now")

        elif action.action.type == "check_equal":
            if game := self._get_game(action.action.game_id, action.user_id):
                if game.active_user == game.user_mapping[action.user_id]:
                    if len(game.bids_history) == 0:
                        self._post_message("It's the first move now, you can't check")
                        return
                    amount = self._get_cubes_amount(game, last_bid)
                    user_name = game.active_user
                    if amount == last_bid.amount:
                        game.users_cubes_count[user_name] += 1
                    else:
                        game.users_cubes_count[user_name] -= 1
                        if game.users_cubes_count[user_name] == 0:
                            self._remove_user(user_name)
                            
                    self._show_game_info(game)
                    self._generate_cubes_in_game(game)
                    self._maputa_handler(game, user_name)
                else:
                    self._post_message("It's not your turn now")

        elif action.action.type == "ask_history":
            if game := self._get_game(action.action.game_id, action.user_id):
                self._post_message("\n".join([f":{bid.value} #{bid.amount}" for bid in game.bids_history]), action.user_id)

    async def _post_message(self, message: str, user: str) -> None:
        print(f"{message}\nto {user}")

    def _get_game(self, game_id, user_id) -> GameState | None:
        game = GAMES_STATES.create(game_id)
        if game:
            return USER_TO_GAME[action.user_id]
        else:
            self._post_message(f"Game with id = \"{game_id}\" not exist", user_id)
            return None
        
    def _show_game_info(self, game: GameState):
        info_str = f"Is maputa: {game.is_maputa}\n"
        for user_name, cubes in game.users_cubes.items():
            # self._post_message(f"You have cubes: {' '.join(cubes.astype(str))}", game.user_mapping_reverse(user_name))
            info_str += f"User {user_name} has cubes: {' '.join(cubes.astype(str))}\n"
        
        for user_name in game.user_mapping.keys():
            self._post_message(info_str, game.user_mapping_reverse[user_name])

    def _generate_cubes_in_game(self, game: GameState):
        game.users_cubes = {
            user_name: np.random.random_integers(1, 7, game.users_cubes_count[user_name]) for user_name in game.user_mapping.values()
        }
        for cubes in game.users_cubes:
            cubes.sort()
        for user_name, cubes in game.users_cubes.items():
            self._post_message(f"You have cubes: {' '.join(cubes.astype(str))}", game.user_mapping_reverse(user_name))

    def _get_next_user(self, game: GameState):
        return min([name for name in game.user_mapping.keys() if name > game.active_user] +
                   [min(game.user_mapping.keys())])

    def _get_prev_user(self, game: GameState):
        return max([name for name in game.user_mapping.keys() if name < game.active_user] +
                   [max(game.user_mapping.keys())])

    def _get_cubes_amount(self, game: GameState, bid: Bid) -> int:
        value = bid.value
        total_amount = 0

        for cubes in game.users_cubes:
            total_amount += (cubes == value).sum()
            if not game.is_maputa and value != JOKER_VALUE:
                total_amount += (cubes == JOKER_VALUE).sum()
        return total_amount

    def _remove_user(self, game, user_name, remove_user=True):
        game.active_user -= 1

        if remove_user:
            USER_TO_GAME.pop(game.user_mapping_reverse[user_name])

        game.user_mapping.pop(action.user_id)
        game.user_mapping_reverse.pop(user_name)

        if game.active_user == user_name:
            game.active_user = self._get_next_user(game)
            
    def _maputa_handler(self, game, user_name):
        if game.users_cubes_count[user_name] == 1 and not game.has_maputa[user_name]:
            game.has_maputa[user_name] = True
            game.is_maputa = True
        else:
            game.is_maputa = False