from abc import ABC, abstractmethod
from typing import Optional

from src.models.game_state import GameState
from src.models.game_status import GameStatus


class GameRepository(ABC):
    @abstractmethod
    def save_game(self, game_state: GameStatus) -> None:
        pass
    
    @abstractmethod
    def load_game(self, game_id: str) -> Optional[GameState]:
        pass
    
    