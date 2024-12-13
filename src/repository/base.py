from abc import ABC, abstractmethod
from typing import Optional

from src.models.game_state import GameState
from src.models.game_status import GameStatus


class GameRepository(ABC):
    """
    Abstract base class for game state persistence.
    """
    @abstractmethod
    def save_game(self, game_state: GameStatus) -> None:
        """
        Save the current game state.
        
        Args:
            game_state: Current state of the game to be persisted
        """
        pass
    
    @abstractmethod
    def load_game(self, game_id: str) -> Optional[GameState]:
        """
        Load a previously saved game state.
        
        Args:
            game_id: Unique identifier of the game to load

        Returns:
            GameState object if found, None otherwise
        """
        pass
    
    