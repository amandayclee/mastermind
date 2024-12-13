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
        self.message = message
        super().__init__(message)
        
    def get_message(self) -> str:
        """Get the error message."""
        return self.message

class GeneratorError(GameError):
    def __init__(self, message: str = "Generator error occurred"):
        self.message = message
        super().__init__(message)
    
    def get_message(self) -> str:
        return self.message
    
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
        self.message = f"Game {game_id} not found"
        super().__init__(self.message)
    
    def get_message(self) -> str:
        return self.message

class DatabaseError(GameError):
    """
    Base class for all database-related errors.
    
    Attributes:
        message (str): Human-readable error message
    """
    def __init__(self, message: str):
        self.message = message
        super().__init__(message)
        
class SaveError(DatabaseError):
    """
    Error raised when database save fails.
    """
    def __init__(self, message: str = "Failed to save the game to database"):
        super().__init__(message)
        
class LoadError(DatabaseError):
    """
    Error raised when database storage fails.
    """
    def __init__(self, message: str = "Failed to load the game to database"):
        super().__init__(message)