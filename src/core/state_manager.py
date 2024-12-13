import logging
from typing import Optional
from src.repository.base import GameRepository
from src.core.models.game_state import GameState
from src.core.models.game_status import GameStatus
from src.services.exceptions.exceptions import GameNotFoundError

logger = logging.getLogger(__name__)

class StateManager:
    """
    Manages the persistence and retrieval of game states.
    
    Attributes:
        repository (GameRepository): The storage backend used for persisting game states
    """
    def __init__(self, repository: GameRepository):
        """
        Initialize a new state manager.
        """
        self.repository = repository
        
    def save_state(self, game_state: GameState) -> None:
        """
        Persist the current game state.
        
        Args:
            game_state: Current state of the game to be saved
        """
        self.repository.save_game(game_state)
        
    def load_state(self, game_id: str) -> Optional[GameStatus]:
        """
        Retrieve a previously saved game state.
        
        Args:
            game_id: Unique identifier of the game to load

        Returns:
            GameStatus object containing the loaded game state

        Raises:
            GameNotFoundError: If no game exists with the given ID
        """
        state = self.repository.load_game(game_id)
        if not state:
            logger.error(f"Game {game_id} not found")
            raise GameNotFoundError(game_id)
        return state
    