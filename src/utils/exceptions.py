from abc import ABC, abstractmethod

class GameError(Exception, ABC):
    """Game error interface - defines error behavior contract"""
    @abstractmethod
    def get_message(self) -> str:
        """All game errors must implement this method"""
        pass

class GuessError(GameError, ABC):
    """Abstract base class for guess related errors"""
    def __init__(self, message: str):
        self._message = message
        super().__init__(self._message)
    
    def get_message(self) -> str:
        return self._message
    
class InvalidLengthError(GuessError):
    def __init__(self, expected_length: int, actual_length: int):
        message = f"Guess must be {expected_length} digits long, got {actual_length}"
        super().__init__(message)

class RangeError(GuessError):
    def __init__(self):
        super().__init__("Numbers must be between 0 and 7")

class GeneratorError(GameError):
    def __init__(self, message: str = "Generator error occurred"):
        self._message = message
        super().__init__(self._message)
    
    def get_message(self) -> str:
        return self._message
    
class GameInitError(GameError):
    def __init__(self, message: str = "Failed to initialize game"):
        self._message = message
        super().__init__(self._message)
    
    def get_message(self) -> str:
        return self._message

class GameNotFoundError(GameError):
    def __init__(self, game_id: str):
        self._message = f"Game {game_id} not found"
        super().__init__(self._message)
    
    def get_message(self) -> str:
        return self._message
