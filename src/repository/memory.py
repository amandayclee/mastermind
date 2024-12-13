from typing import Optional
from src.core.models.game_state import GameState
from src.repository.base import GameRepository
import logging


logger = logging.getLogger(__name__)


class InMemoryGameRepository(GameRepository):
    """
    In memeory implementation of the game repository for storing and retrieving game states.
    """
    def __init__(self):
        """
        Initialize InMemoryGameRepository with a dictionary.
        
        Args:
            _store (dict): 
        """
        self._store = {}
        
    def save_game(self, game_state: GameState) -> None:
        """
        Save or update a game state in memory
    
        Args:
            game_state (GameState): The game state to save            
        """
        game_id = game_state.game_id
        self._store[game_id] = game_state.to_db_format()
        logger.debug("Game state saved successfully")
    
    
    def load_game(self, game_id: str) -> Optional[GameState]:
        """
        Load a game state from in memory by its ID.
        
        Args:
            game_id (str): The unique identifier of the game to load
            
        Returns:
            GameState: The loaded game state
        """
        stored_data = self._store.get(game_id)
        
        if stored_data is None:
            logger.warning("Game not found - ID: %s", game_id)
            return None
            
        logger.debug("Game state loaded successfully")
        return GameState.from_db_format(stored_data)