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

class GuessError(GameError):
    """Base class for all guess-related errors."""
    def __init__(self, message: str):
        super().__init__(message)

    
class InvalidLengthError(GuessError):
    """
    Error raised when a guess has an incorrect number of digits.
    
    Attributes:
        expected_length (int): The required length of the guess
        actual_length (int): The actual length of the provided guess
    """
    def __init__(self, expected_length: int, actual_length: int):
        """
        Initialize a new invalid length error.
        
        Args:
            expected_length: The required number of digits
            actual_length: The actual number of digits provided
        """
        self.expected_length = expected_length
        self.actual_length = actual_length
        message = f"Guess must be {expected_length} digits long, got {actual_length}"
        super().__init__(message)

class RangeError(GuessError):
    """
    Error raised when a guess contains numbers outside the valid range.
    
    Attributes:
        value (int): The invalid value
        min_value (int): Minimum allowed value
        max_value (int): Maximum allowed value
    """
    def __init__(self, value: int, min_value: int = 0, max_value: int = 7):
        self.value = value
        self.min_value = min_value
        self.max_value = max_value
        message = f"Number {value} must be between {min_value} and {max_value}"
        super().__init__(message)

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