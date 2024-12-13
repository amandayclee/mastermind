import logging

from src.core.models.game_difficulty import Difficulty


logger = logging.getLogger(__name__)

class GameConfig():
    """
    Configuration class for the Mastermind game settings.
    
    This class holds all configurable parameters for a game instance, allowing
    for flexible game rules and difficulty settings.
    
    Attributes:
        difficulty (Difficulty): The game's difficulty level (normal or hard)
        pattern_length (int): Length of the code pattern to guess (default: 4)
        min_number (int): Minimum value for each digit in the pattern (default: 0)
        max_number (int): Maximum value for each digit in the pattern (default: 7)
        max_attempts (int): Maximum number of guess attempts allowed (default: 10)
    """
    def __init__(self, difficulty: Difficulty = Difficulty.NORMAL) -> None:
        """
        Initialize a new game configuration.
        
        Args:
        pattern_length (int): Length of the code pattern to guess (default: 4)
        min_number (int): Minimum value for each digit in the pattern (default: 0)
        max_number (int): Maximum value for each digit in the pattern (default: 7)
        max_attempts (int): Maximum number of guess attempts allowed (default: 10)
        """
        self.difficulty = difficulty
        
        if difficulty == Difficulty.NORMAL:
            self.pattern_length = 4
            self.min_number = 0
            self.max_number = 7
            self.max_attempts = 10
        elif difficulty == Difficulty.HARD:
            self.pattern_length = 5
            self.min_number = 0
            self.max_number = 9
            self.max_attempts = 8