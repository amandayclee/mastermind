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
    """
    Represents a Mastermind game session that manages game state and rules.
    
    The Game class serves as the central coordinator for a Mastermind game session,
    handling game initialization, state management, guess validation, and game progression.
    It interacts with various components:
    - StateManager: Handles saving/loading game states
    - GameLogic: Implements core game rules and calculations
    - NumberGenerator: Provides the secret code pattern
    - GameRepository: Manages persistence of game states
    
    Attributes:
        state_manager (StateManager): Manages game state persistence
        config (GameConfig): Game configuration settings
        game_logic (GameLogic): Core game rules implementation
        game_id (str): Unique identifier for this game session
        code_pattern (List[int]): Secret code players try to guess
        pattern_count (dict): Count of each number in code pattern
        status (GameStatus): Current game status
        attempts (int): Number of guesses made
        guess_records (List[Tuple[Guess, Feedback]]): History of guesses and feedback
        created_at (datetime): When the game was created
        updated_at (datetime): When the game was updated by a new guess or exit
    """
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
  
    def initialize_new_game(self, generator) -> None:
        """
        Set up a new game with fresh state.
        
        Creates a new game ID, generates the code pattern, and initializes
        game state variables.
        
        Args:
            generator: Number generator to create secret code
        """
        self.game_id = str(uuid.uuid4())
        self.code_pattern = self.game_logic.generate_code_pattern(generator)
        self.pattern_count = self.game_logic.calculate_pattern_counts(self.code_pattern)
        self.status = GameStatus.IN_PROGRESS
        self.attempts = 0
        self.guess_records = []
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        
    def _save_current_state(self) -> None:
        """
        Creates a GameState object capturing all current game information and saves it
        using the state manager. This ensures game progress can be restored later.
        """
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
        """
        Retrieves the current game status.
        
        Returns:
            str: Current game status (in_progress, won, or lost)
        """
        return self.status
    
    def get_code_pattern(self) -> List[int]:
        """
        Retrieves a copy of the secret code pattern.
        
        Returns:
            List[int]: Copy of the secret code pattern to prevent direct modification
        """
        return self.code_pattern.copy()
    
    def get_guess_history(self) -> List[Tuple[Guess, Feedback]]:
        """
        Retrieves the complete history of guesses and their feedback.
        
        Returns:
            List[Tuple[Guess, Feedback]]: List of (guess, feedback) pairs in chronological order
        """
        return self.guess_records.copy()
    
    def get_remaining_attempts(self) -> int:
        """
        Calculates how many guess attempts remain.
        
        Returns:
            int: Number of remaining attempts allowed
        """
        return self.config.max_attempts - self.attempts
    
    def validate_guess_input(self, guess_input: str) -> Guess:
        """
        Validates and converts a string input into a valid guess.
        
        Performs several validation checks:
        1. Input is not empty
        2. All characters are numeric
        3. Length matches the code pattern length
        4. All numbers are within allowed range
        
        Args:
            guess_input (str): String of numbers from player input
            
        Returns:
            Guess: Valid guess object
            
        Raises:
            GuessError: If input is empty or non-numeric
            InvalidLengthError: If input length doesn't match code length
            RangeError: If any number is outside allowed range
        """
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
                raise RangeError(num, self.config.min_number, self.config.max_number)
                
        return Guess(numbers)
    
    def make_guess(self, guess: Guess) -> Feedback:
        """
        Processes a player's guess and updates game state.
        
        This is the core game mechanic that:
        1. Evaluates the guess against the code pattern
        2. Generates appropriate feedback
        3. Updates game history
        4. Checks for win/loss conditions
        5. Saves the updated state
        
        Args:
            guess (Guess): The player's guess to evaluate
            
        Returns:
            Feedback: Information about correct numbers and positions
        """
        logger.info(f"Processing guess: {guess}")
    
        feedback = self.game_logic.check_guess(guess, self.pattern_count, self.code_pattern)
        
        self.guess_records.append((guess, feedback))
        self.attempts += 1
    
        self._update_game_state(feedback)    
        self._save_current_state()
        
    def _update_game_state(self, feedback: Feedback) -> None:
        """
        Updates game status based on the latest guess result.
        
        Determines if the game has been won or lost based on:
        - Whether all numbers are in correct positions (win)
        - Whether maximum attempts have been reached (loss)
        
        Args:
            feedback (Feedback): The feedback from the latest guess
        """
        if feedback.is_winning_guess(self.config.pattern_length):
            self.status = GameStatus.WON
        elif self.attempts >= self.config.max_attempts:
            self.status = GameStatus.LOST
            
    def _restore_state(self, state: GameState) -> None:
        """
        Restores a game from a saved state.
        
        Reconstructs all game attributes from a GameState object, including:
        - Game identification
        - Secret code and pattern counts
        - Current status and attempts
        - Guess history
        - Configuration
        
        Args:
            state (GameState): Saved game state to restore from
        """
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