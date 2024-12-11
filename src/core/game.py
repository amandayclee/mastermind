from datetime import datetime
import logging
from typing import List, Tuple
import uuid
from src.models.game_state import GameState
from src.core.repository.base import GameRepository
from src.core.repository.memory import InMemoryGameRepository
from src.core.generators.base import NumberGenerator
from src.core.generators.random_org import RandomOrgGenerator
from src.models.game_status import GameStatus
from src.models.guess import Guess
from src.models.feedback import Feedback
from src.config.game_config import GameConfig
from src.utils.exceptions import GameNotFoundError, GameInitError, GeneratorError, GuessError, InvalidLengthError, RangeError

logger = logging.getLogger(__name__)

class Game:
    def __init__(self, 
                 generator: NumberGenerator=RandomOrgGenerator(), repository: GameRepository = InMemoryGameRepository(), game_id: str = None) -> None:
        self.repository = repository
        
        if game_id:
            logger.info("Reload old game state")
            state = self.repository.load_game(game_id)
            if not state:
                logger.error(f"Game {game_id} not found")
                raise GameNotFoundError(game_id)
            self._restore_state(state)
        else:
            logger.info("Initializing new game")
            self.game_id = str(uuid.uuid4()) 
            self.config = GameConfig()
            self.status = GameStatus.IN_PROGRESS
            self.pattern_count = {}
            self.generator = generator
            self.code_pattern = self._generate_code_pattern()
            self.attempts = 0
            self.guess_records = []
            self.created_at = datetime.now()
            self._save_state()
        
    def is_active(self) -> bool:
        return self.status == GameStatus.IN_PROGRESS
    
    def is_won(self) -> bool:
        return self.status == GameStatus.WON

    def get_remaining_attempts(self) -> int:
        return self.config.max_attempts - self.attempts
    
    def get_guess_history(self) -> List[Tuple[Guess, Feedback]]:
        return self.guess_records.copy()
    
    def validate_guess_input(self, guess_input: str) -> List[int]:
        """Validate the raw input string"""
        if not guess_input.strip():
            logger.warning("Empty input received")
            raise GuessError("Input cannot be empty")
        
        try:
            numbers = [int(x) for x in guess_input]
        except ValueError:
            logger.warning(f"Non-numeric input received: {guess_input}")
            raise GuessError("Input must be numbers")
            
        if len(numbers) != len(self.code_pattern):
            logger.warning(f"Invalid length: expected {len(self.code_pattern)}, got {len(numbers)}")
            raise InvalidLengthError(len(self.code_pattern), len(numbers))
            
        for num in numbers:
            if num < self.config.min_number or num > self.config.max_number:
                logger.warning(f"INumbers must be between 0 and 7: {guess_input}")
                raise RangeError()
                
        return numbers

    def create_guess(self, numbers: List[int]) -> Guess:
        """Create a valid Guess object from validated numbers"""
        return Guess(numbers)

    def make_guess(self, guess: Guess) -> Feedback:
        """Handle a guess and update game status"""
        logger.info(f"Processing guess: {guess}")
        correct_number, correct_location = self._check_guess(guess)
        feedback = Feedback(correct_number, correct_location)
        
        self.guess_records.append((guess, feedback))
        self.attempts += 1
        
        logger.info(f"Attempt {self.attempts}: Feedback - {feedback}")
        self._update_game_state(feedback)
        self._save_state()
        return feedback

    def _generate_code_pattern(self) -> List[int]:
        """generator injection"""
        try:
            code_pattern = self.generator.generate(self.config)
            logger.info("Code pattern generated successfully")
            self._calculate_pattern_counts(code_pattern)
            return code_pattern
        except GeneratorError as e:
            logger.error(f"Failed to generate code pattern: {e}")
            raise GameInitError(f"Failed to initialize game: {e}")
        
    def _calculate_pattern_counts(self, code_pattern: List[int]) -> None:
        for num in code_pattern:
            self.pattern_count[num] = self.pattern_count.get(num, 0) + 1
              
    def _update_game_state(self, feedback: Feedback) -> None:
        """Update game state after make a guess"""
        if feedback.is_winning_guess(self.config.pattern_length):
            self.status = GameStatus.WON
        elif self.attempts >= self.config.max_attempts:
            self.status = GameStatus.LOST
        
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
    
    def _save_state(self) -> None:
        state = GameState(
            game_id = self.game_id,
            code_pattern = self.code_pattern,
            status = self.status,
            attempts = self.attempts,
            guess_records = self.guess_records,
            created_at = self.created_at,
            updated_at = datetime.now(),
            config = self.config
        )
        self.repository.save_game(state)
        
    def _restore_state(self, state: GameState) -> None:
        self.game_id = state.game_id
        self.code_pattern = state.code_pattern
        self.status = state.status
        self.attempts = state.attempts
        self.guess_records = state.guess_records
        self.created_at = state.created_at
        self.config = state.config
        
        self.pattern_count = {}
        for num in self.code_pattern:
            self.pattern_count[num] = self.pattern_count.get(num, 0) + 1