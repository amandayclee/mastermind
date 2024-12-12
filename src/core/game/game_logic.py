import logging
from typing import Dict, List, Tuple
from src.models.feedback import Feedback
from src.models.guess import Guess
from src.core.generators.base import NumberGenerator
from src.config.game_config import GameConfig
from src.utils.exceptions import GameInitError, GeneratorError

logger = logging.getLogger(__name__)
class GameLogic:
    def __init__(self, config: GameConfig):
        self.config = config
        
    def generate_code_pattern(self, generator: NumberGenerator) -> List[int]:
        try:
            code_pattern = generator.generate(self.config)
            logger.info("Code pattern generated successfully")
            return code_pattern
        except GeneratorError as e:
            logger.error(f"Failed to generate code pattern: {e}")
            raise GameInitError(f"Failed to initialize game: {e}")
        
    def calculate_pattern_counts(self, code_pattern: List[int]) -> Dict[int, int]:
        pattern_count = {}
        for num in code_pattern:
            pattern_count[num] = pattern_count.get(num, 0) + 1
        return pattern_count
    
    def check_guess(self, guess: Guess, pattern_count: Dict[int, int], code_pattern: List[int]) -> Feedback:
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