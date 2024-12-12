import logging
from typing import Optional
from src.core.repository.base import GameRepository
from src.models.game_state import GameState
from src.models.game_status import GameStatus
from src.utils.exceptions import GameNotFoundError

logger = logging.getLogger(__name__)

class StateManager:
    def __init__(self, repository: GameRepository):
        self.repository = repository
        
    def save_state(self, game_state: GameState) -> None:
        self.repository.save_game(game_state)
        
    def load_state(self, game_id: str) -> Optional[GameStatus]:
        state = self.repository.load_game(game_id)
        if not state:
            logger.error(f"Game {game_id} not found")
            raise GameNotFoundError(game_id)
        return state
    