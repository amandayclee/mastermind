from datetime import datetime
import logging
from typing import List, Optional, Tuple
import uuid
from src.config.game_config import GameConfig
from src.core.generators.random_org import RandomOrgGenerator
from src.core.repository.memory import InMemoryGameRepository
from src.models.feedback import Feedback
from src.models.game_state import GameState
from src.models.game_status import GameStatus
from src.models.guess import Guess
from src.core.game.game_logic import GameLogic
from src.core.game.state_manager import StateManager
from src.core.generators.base import NumberGenerator
from src.core.repository.base import GameRepository
from src.utils.exceptions import GuessError, InvalidLengthError, RangeError

logger = logging.getLogger(__name__)

class Game:
    def __init__(self, 
                 repository: GameRepository = InMemoryGameRepository(), 
                 generator: NumberGenerator = RandomOrgGenerator(), 
                 game_id: str = None,
                 config: Optional[GameConfig] = None):
        self.state_manager = StateManager(repository)
        self.config = config or GameConfig()
        self.game_logic = GameLogic(self.config)
        
        if game_id:
            state = self.state_manager.load_state(game_id)
            self._restore_state(state)
        else:
            self.initialize_new_game(generator)
            self._save_current_state()
  
    def initialize_new_game(self, generator):
        self.game_id = str(uuid.uuid4())
        self.code_pattern = self.game_logic.generate_code_pattern(generator)
        self.pattern_count = self.game_logic.calculate_pattern_counts(self.code_pattern)
        self.status = GameStatus.IN_PROGRESS
        self.attempts = 0
        self.guess_records = []
        self.created_at = datetime.now()
        
    def _save_current_state(self):
        state = GameState(
            game_id=self.game_id,
            code_pattern=self.code_pattern,
            status=self.status,
            attempts=self.attempts,
            guess_records=self.guess_records,
            created_at=self.created_at,
            updated_at=datetime.now(),
            config=self.config
        )
        self.state_manager.save_state(state)
    
    def get_status(self) -> str:
        return self.status
    
    def get_code_pattern(self) -> List[int]:
        return self.code_pattern.copy()
    
    def get_guess_history(self) -> List[Tuple[Guess, Feedback]]:
        return self.guess_records.copy()
    
    def get_remaining_attempts(self) -> int:
        return self.config.max_attempts - self.attempts
    
    def validate_guess_input(self, guess_input: str) -> Guess:
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
                
        return Guess(numbers)
    
    def make_guess(self, guess: Guess) -> Feedback:
        """Processes a player's guess and returns feedback"""
        logger.info(f"Processing guess: {guess}")
    
        feedback = self.game_logic.check_guess(guess, self.pattern_count, self.code_pattern)
        
        self.guess_records.append((guess, feedback))
        self.attempts += 1
    
        self._update_game_state(feedback)    
        self._save_current_state()
        
    def _update_game_state(self, feedback: Feedback) -> None:
        """Update game state after make a guess"""
        if feedback.is_winning_guess(self.config.pattern_length):
            self.status = GameStatus.WON
        elif self.attempts >= self.config.max_attempts:
            self.status = GameStatus.LOST
            
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