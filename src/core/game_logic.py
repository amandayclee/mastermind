import logging
from typing import Dict, List, Tuple
from src.core.models.feedback import Feedback
from src.core.models.guess import Guess
from src.services.generators.base import NumberGenerator
from src.core.config.game_config import GameConfig
from src.services.exceptions.exceptions import GameInitError, GeneratorError

logger = logging.getLogger(__name__)

class GameLogic:
    """
    Handles the core game logic for the Mastermind game.
    
    This class manages the game's core functionality including code pattern generation,
    guess validation, and feedback calculation. It uses dependency injection for number
    generation and maintains game configuration.
    
    Attributes:
        config (GameConfig): Configuration settings for the game including code length, value ranges, and maximum attempts.
    """
    def __init__(self, config: GameConfig):
        """
        Initialize the GameLogic instance with game configuration.
        
        Args:
            config (GameConfig): Configuration object containing game settings.
        """
        self.config = config
        
    def generate_code_pattern(self, generator: NumberGenerator) -> List[int]:
        """
        Generate a secret code pattern using the provided number generator.
        
        Args:
            generator (NumberGenerator): Implementation of number generator interface.
            
        Returns:
            List[int]: Generated code pattern as a list of integers.
            
        Raises:
            GameInitError: If code pattern generation fails.
        """
        
        try:
            code_pattern = generator.generate(self.config)
            logger.info("Code pattern generated successfully")
            return code_pattern
        except GeneratorError as e:
            logger.error(f"Failed to generate code pattern: {e}")
            raise GameInitError(f"Failed to initialize game: {e}")
        
    def calculate_pattern_counts(self, code_pattern: List[int]) -> Dict[int, int]:
        """
        Creates a dictionary mapping each number to its frequency in the pattern.
        
        Args:
            code_pattern (List[int]): The secret code pattern to analyze.
            
        Returns:
            Dict[int, int]: Dictionary mapping numbers to their frequencies.
        """
        
        pattern_count = {}
        for num in code_pattern:
            pattern_count[num] = pattern_count.get(num, 0) + 1
        return pattern_count
    
    def check_guess(self, guess: Guess, pattern_count: Dict[int, int], code_pattern: List[int]) -> Feedback:
        """
        Compares the guess against the code pattern and generates feedback indicating
        the number of correct digits (right number, wrong position) and correct positions
        (right number, right position).
        
        Args:
            guess (Guess): The player's guess containing the numbers to check.
            pattern_count (Dict[int, int]): Frequency map of numbers in code pattern.
            code_pattern (List[int]): The secret code pattern to compare against.
            
        Returns:
            Feedback: Object containing the number of correct digits and positions.
        """
        guess_numbers = guess.get_numbers()
        current_pattern_count = pattern_count.copy()
        
        correct_location = 0
        correct_number = 0
        
        for idx in range(len(guess_numbers)):
            if guess_numbers[idx] == code_pattern[idx]:
                correct_location += 1
                
        for guess_num in guess_numbers:
            if guess_num in current_pattern_count and current_pattern_count[guess_num] > 0:
                correct_number += 1
                current_pattern_count[guess_num] -= 1
        
        return Feedback(correct_number, correct_location)