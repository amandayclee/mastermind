from abc import ABC
import logging

logger = logging.getLogger(__name__)

class GameError(Exception, ABC):
    """
    Base abstract class for all game-related exceptions.
    
    Provides a common interface for handling game errors and enforces
    implementation of error message retrieval.
    
    Attributes:
        message (str): Human-readable error message
    """
    def __init__(self, message: str):
        logger.error("Game error occurred: %s", message)
        super().__init__(message)

class GeneratorError(GameError):
    def __init__(self, message: str = "Generator error occurred"):
        super().__init__(message)
    
class GameInitError(GameError):
    """Error raised when number generation fails."""
    def __init__(self, message: str = "Generator error occurred"):
        super().__init__(message)
        
class GameNotFoundError(GameError):
    """
    Error raised when attempting to load a non-existent game.
    
    Attributes:
        game_id (str): ID of the game that couldn't be found
    """
    def __init__(self, game_id: str):
        message = f"Game {game_id} not found"
        logger.error("Game lookup failed: %s", self.message)
        super().__init__(message)
    

class DatabaseError(GameError):
    """
    Base class for all database-related errors.
    """
    pass
        
class SaveError(DatabaseError):
    """
    Error raised when database save fails.
    """
    def __init__(self, message: str = "Failed to save the game to database"):
        logger.error("Game save failed: %s", message)
        super().__init__(message)
        
class LoadError(DatabaseError):
    """
    Error raised when database storage fails.
    """
    def __init__(self, message: str = "Failed to load the game to database"):
        logger.error("Game load failed: %s", message)
        super().__init__(message)