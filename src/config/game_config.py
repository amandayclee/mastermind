import logging


logger = logging.getLogger(__name__)

class GameConfig():
    """
    Configuration class for the Mastermind game settings.
    
    This class holds all configurable parameters for a game instance, allowing
    for flexible game rules and difficulty settings.
    
    Attributes:
        pattern_length (int): Length of the code pattern to guess (default: 4)
        min_number (int): Minimum value for each digit in the pattern (default: 0)
        max_number (int): Maximum value for each digit in the pattern (default: 7)
        max_attempts (int): Maximum number of guess attempts allowed (default: 10)
    """
    def __init__(self, 
                 pattern_length: int = 4, 
                 min_number: int = 0, 
                 max_number: int = 7, 
                 max_attempts: int = 10) -> None:
        """
        Initialize a new game configuration.
        
        Args:
        pattern_length (int): Length of the code pattern to guess (default: 4)
        min_number (int): Minimum value for each digit in the pattern (default: 0)
        max_number (int): Maximum value for each digit in the pattern (default: 7)
        max_attempts (int): Maximum number of guess attempts allowed (default: 10)
        """
        self.pattern_length = pattern_length
        self.min_number = min_number
        self.max_number = max_number
        self.max_attempts = max_attempts