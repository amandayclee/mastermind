import logging
from typing import List
from src.core.config.game_config import GameConfig

logger = logging.getLogger(__name__)

class ValidationResult:
    """
    Represents the outcome of a validation check.
    
    Attributes:
        is_valid: Whether the validation passed
        message: Human-readable error message if validation failed
        error_code: Machine-readable error code for programmatic handling
    """
    
    def __init__(self, is_valid: bool, message: str = "", error_code = ""):
        self.is_valid = is_valid
        self.message = message
        self.error_code = error_code

class InputValidator:
    """
    Handles validation of user input for the Mastermind game.
    
    This class centralizes all input validation logic, making it easier to:
    1. Maintain consistent validation rules
    2. Provide clear error messages
    3. Add new validation rules as needed
    
    The validator is stateless, so a single instance can be reused
    across multiple game sessions.
    """
    def __init__(self, config: GameConfig = GameConfig()):
        """
        Initialize validator with game configuration.
        
        Args:
            config: Game configuration containing rules for validation
        """
        self.config = config
        logger.debug("Initialized input validator with config: pattern_length=%d",
            config.pattern_length)
        
    def validate_guess_input(self, guess_input: str) -> ValidationResult:
        """
        Validates raw user input for a guess before conversion to numbers.
        
        This is the first validation step that checks the basic string format
        before attempting to convert to numbers.
        
        Args:
            guess_input: Raw string input from user
            
        Returns:
            ValidationResult indicating whether input is valid and why if not
        """
        logger.debug("Validating guess input: %s", guess_input)
        
        if not guess_input.strip():
            return ValidationResult(
                is_valid=False,
                message="Input cannot be empty",
                error_code="EMPTY_INPUT"
            )
            
        if " " in guess_input:
            numbers = guess_input.split()
        else:
            numbers = list(guess_input)

        if not all(c.isdigit() or c.isspace() for c in guess_input):
            return ValidationResult(
                is_valid=False,
                message="Input must contain only numbers",
                error_code="NON_NUMERIC"
            )

        if len(numbers) != self.config.pattern_length:
            return ValidationResult(
                is_valid=False,
                message=f"Must enter exactly {self.config.pattern_length} numbers",
                error_code="INVALID_LENGTH"
            )
            
        logger.debug("Guess input format validation successful")
        return ValidationResult(is_valid=True)
    
    def validate_number_range(self, numbers: List[int]) -> ValidationResult:
        """
        Validates that all numbers are within the allowed range.
        
        Args:
            numbers: List of numbers to validate
            
        Returns:
            ValidationResult indicating whether numbers are valid
        """
        for num in numbers:
            if num < self.config.min_number or num > self.config.max_number:
                return ValidationResult(
                    is_valid=False,
                    message=f"Numbers must be between {self.config.min_number} "
                           f"and {self.config.max_number}",
                    error_code="OUT_OF_RANGE"
                )
        logger.debug("Guess input range validation successful")
        return ValidationResult(is_valid=True)
    
    def validate_game_id(self, game_id: str) -> ValidationResult:
        """
        Validates a game ID format.
        
        Checks that the game ID is not empty and follow uuid's rule.
        
        Args:
            game_id: The game ID to validate
            
        Returns:
            ValidationResult indicating whether ID is valid
        """
        if not game_id:
            return ValidationResult(
                is_valid=False,
                message="Game ID cannot be empty",
                error_code="EMPTY_ID"
            )

        if not game_id.strip():
            return ValidationResult(
                is_valid=False,
                message="Game ID cannot be only whitespace",
                error_code="WHITESPACE_ID"
            )

        if len(game_id) != 36 or not all(c.isalnum() or c == '-' for c in game_id):
            return ValidationResult(
                is_valid=False,
                message="Invalid game ID format",
                error_code="INVALID_ID_FORMAT"
            )

        logger.debug("Game ID validation successful")
        return ValidationResult(is_valid=True)
    
    def validate_difficulty_selection(self, selection: str) -> ValidationResult:
        """
        Validates user's difficulty selection input.
        
        Args:
            selection: The user's input for difficulty selection
            
        Returns:
            ValidationResult indicating whether selection is valid
        """
        if not selection.strip():
            return ValidationResult(
                is_valid=False,
                message="Please select a difficulty level",
                error_code="EMPTY_SELECTION"
            )

        if selection not in ["1", "2"]:
            return ValidationResult(
                is_valid=False,
                message="Please select 1 for Normal or 2 for Hard",
                error_code="INVALID_DIFFICULTY"
            )

        logger.debug("Difficulty selection validation successful")
        return ValidationResult(is_valid=True)
    
    def update_config(self, new_config: GameConfig) -> None:
        """
        Update validator configuration.
        Called when starting a new game or loading a saved game.
        
        Args:
            new_config: New game configuration to use for validation
        """
        self.config = new_config
        
        logger.debug("Update config after loading successful")