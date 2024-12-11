from typing import Optional
from src.models.game_state import GameState
from src.core.repository.base import GameRepository


class InMemoryGameRepository(GameRepository):
    def __init__(self):
        self._state = {}
        
    def save_game(self, game_state: GameState) -> str:
        game_id = game_state.game_id
        self._store[game_id] = game_state
        return game_id
    
    def load_game(self, game_id: str) -> Optional[GameState]:
        stored_data = self._store.get(game_id)

        if stored_data is not None:
            return GameState.from_db_format(stored_data)
        
        return None