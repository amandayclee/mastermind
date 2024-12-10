from typing import List, Tuple
from src.core.generators.base import NumberGenerator
from src.core.generators.random_org import RandomOrgGenerator
from src.models.guess import Guess
from src.models.feedback import Feedback
from src.config.game_config import GameConfig
from src.utils.exceptions import GameInitError, GeneratorError, GuessError, InvalidLengthError, RangeError

class Game:
    def __init__(self, generator: NumberGenerator=RandomOrgGenerator()) -> None:
        self.config = GameConfig()
        self._is_active = True
        self._is_won = False
        self.pattern_count = {}
        self.generator = generator
        self.code_pattern = self._generate_code_pattern()
        self.attempts = 0
        self.guess_records = []
        
    def is_active(self) -> bool:
        return self._is_active
    
    def is_won(self) -> bool:
        return self._is_won

    def get_remaining_attempts(self) -> int:
        return self.config.max_attempts - self.attempts
    
    def get_guess_history(self) -> List[Tuple[Guess, Feedback]]:
        return self.guess_records.copy()
    
    def validate_guess_input(self, guess_input: str) -> List[int]:
        """Validate the raw input string"""
        if not guess_input.strip():
            raise GuessError("Input cannot be empty")
        
        try:
            numbers = [int(x) for x in guess_input]
        except ValueError:
            raise GuessError("Input must be numbers")
            
        if len(numbers) != len(self.code_pattern):
            raise InvalidLengthError(len(self.code_pattern), len(numbers))
            
        for num in numbers:
            if num < self.config.min_number or num > self.config.max_number:
                raise RangeError()
                
        return numbers

    def create_guess(self, numbers: List[int]) -> Guess:
        """Create a valid Guess object from validated numbers"""
        return Guess(numbers)

    def make_guess(self, guess: Guess) -> Feedback:
        """Handle a guess and update game status"""
        correct_number, correct_location = self._check_guess(guess)
        feedback = Feedback(correct_number, correct_location)
        
        self.guess_records.append([guess, feedback])
        self.attempts += 1
        
        self._update_game_state(feedback)
        return feedback

    def _generate_code_pattern(self) -> List[int]:
        """generator injection"""
        try:
            code_pattern = self.generator.generate(self.config)
            self._calculate_pattern_counts(code_pattern)
            return code_pattern
        except GeneratorError as e:
            raise GameInitError(f"Failed to initialize game: {e}")
        
    def _calculate_pattern_counts(self, code_pattern: List[int]) -> None:
        for num in code_pattern:
            self.pattern_count[num] = self.pattern_count.get(num, 0) + 1
              
    def _update_game_state(self, feedback: Feedback) -> None:
        """Update game state after make a guess"""
        if feedback.is_winning_guess(self.config.pattern_length):
            self._is_won = True
            self._is_active = False
        elif self.attempts >= self.config.max_attempts:
            self._is_active = False
        
    def _check_guess(self, guess: Guess) -> Tuple[int, int]:
        """Check both number and location correctness in one pass"""
        guess_numbers = guess.get_numbers()
        pattern_count = self.pattern_count.copy()
        correct_location = 0
        correct_number = 0
        
        for idx in range(len(guess_numbers)):
            if guess_numbers[idx] == self.code_pattern[idx]:
                correct_location += 1

        for guess_num in guess_numbers:
            if guess_num in pattern_count and pattern_count[guess_num] > 0:
                correct_number += 1
                pattern_count[guess_num] -= 1
                
        return correct_number, correct_location