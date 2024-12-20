import logging
from src.core.config.game_config import GameConfig
from src.core.models.guess import Guess
from src.repository.sqlite import SQLiteGameRepository
from src.repository.base import GameRepository
from src.core.models.game_status import GameStatus
from src.core.game import Game
from src.services.exceptions.exceptions import GameInitError, GameNotFoundError
from src.core.models.game_difficulty import Difficulty
from src.utils.validators import InputValidator

logger = logging.getLogger(__name__)

class GameInterface:
    def __init__(self, repository: GameRepository = SQLiteGameRepository()) -> None:
        """
        Initialize a new game interface.
        
        Args:
            game (Game): Reference to the current game instance being played
            repository (GameRepository): Repository for game state persistence
            repository(InputValidator): Utility to validate user input
        """
        self.game = None
        self.repository = repository
        self.validator = InputValidator(GameConfig())
        
    def start_menu(self) -> None:
        """
        Start the main menu loop.
        
        Displays the main menu and handles user navigation including:
        - Starting new games
        - Loading existing games
        - Exiting the program
        
        The menu continues to loop until the user chooses to exit.
        """
        logger.info("Starting main menu")
        while True:
            print("\n****** Mastermind ******")
            print("1. New Game")
            print("2. Load Game")
            print("3. Exit Program")
            choice = input("Select an option (1-3): ")
            logger.debug("User selected menu option: %s", choice)
            
            if choice == "1":
                self._handle_new_game()
            elif choice == "2":
                self._handle_load_game()
            elif choice == "3":
                logger.info("User chose to exit program")
                print("Thanks for playing!")
                break
            else:
                logger.warning("Invalid menu choice: %s", choice)
                print("Invalid choice. Please select 1, 2, or 3")
                
    def _handle_new_game(self) -> None:
        """
        Handle the creation of a new game.
        """
        try: 
            difficulty = self._select_difficulty()
            config = GameConfig(difficulty=difficulty)
            self.validator = InputValidator(config)
            self.game = Game(repository=self.repository, config=config)
            logger.info("New game created with ID: %s", self.game.game_id)
            
            print(f"\nYour game ID is: {self.game.game_id}")
            print("Keep this ID if you want to continue this game later!\n")
            self.run_game()
        except GameInitError:
            logger.warning("Attempted to initialize a game but failed. Try again.")
            return
        
    def _handle_load_game(self) -> None:
        """
        Handle loading of an existing game.
        """
        while True:
            game_id = input("Enter your game ID (or 'exit' to return to menu): ").strip()
            
            if game_id.lower() == 'exit':
                print("Returning to main menu...\n")
                break
                
            id_result = self.validator.validate_game_id(game_id)
            if not id_result.is_valid:
                logger.warning("Invalid game ID format: %s", game_id)
                print(id_result.message)
                continue
            
            try:
                self.game = Game(repository=self.repository, game_id=game_id)
                self.validator.update_config(self.game.config)
                logger.info("Successfully loaded game: %s", game_id)
                self.run_game()
                break  
            except GameNotFoundError:
                logger.warning("Attempted to load non-existent game: %s", game_id)
                print(f"Game with ID '{game_id}' not found.\n")
                print("Please try again or type 'exit' to return to the main menu.\n")
    
    def run_game(self) -> None:
        """
        Run the main game loop.
        """
        logger.info("Starting game session")
        print("Type 'exit' to return to main menu")
        print("Type 'id' to see your game ID")
        
        while self.game.get_status() == GameStatus.IN_PROGRESS:
            self._display_game_state()
            guess_input = input(f"Please enter {self.game.config.pattern_length} numbers with each number is between {self.game.config.min_number} and {self.game.config.max_number}:\n")
            
            if guess_input == 'id':
                print(f"\nYour game ID is: {self.game.game_id}")
                continue
            elif guess_input == 'exit':
                logger.info("User chose to exit current game: %s", self.game.game_id)
                print(f"\nExiting game. Your game ID is: {self.game.game_id}")
                print("Use this ID to continue your game later!")
                return
            
            self.process_guess_input(guess_input)
                            
        self._display_game_result()
            
    def process_guess_input(self, guess_input: str) -> None:
        """
        Process and validate user's guess input.
        
        Args:
            guess_input (str): The user's input string containing their guess

        """
        
        format_result = self.validator.validate_guess_input(guess_input)
        if not format_result.is_valid:
            logger.warning("Invalid guess format: %s", guess_input)
            print(format_result.message)
            return
        
        numbers = self.validator.parse_guess_input(guess_input)
        
        range_result = self.validator.validate_number_range(numbers)
        if not range_result.is_valid:
            logger.warning("Numbers out of valid range: %s", numbers)
            print(range_result.message)
            return

        # If all validation passes, make the guess
        self.game.make_guess(Guess(numbers))
        logger.info("Valid guess processed: %s", numbers)

            
    def _display_game_state(self) -> None:
        """
        Display the current game state.
        
        Shows:
        - History of previous guesses and their feedback
        - Number of remaining attempts
        """
        
        guess_records = self.game.get_guess_history() 
        attempts_left = self.game.get_remaining_attempts()
        
        if guess_records:
            print("\n====== Previous Guesses ======")
        
        for record in guess_records:
            print(f"Player guesses \"{record[0]}\", {record[1]}")

        print(f"\nAttempts remaining: {attempts_left}\n")
        logger.debug("Game state displayed - Attempts left: %d", attempts_left)
            
    def _display_game_result(self) -> None:
        """
        Display the final game result.
        
        Shows:
        - Win/loss message
        - The secret code pattern (if the player lost)
        """
        status = self.game.get_status()
        logger.info("Game ended with status: %s", status)
        
        print("\n========= Game Over =========")
        if self.game.get_status() == GameStatus.WON:
            print("Congrats! You win the game!")
        else:
            print("Game Over! Better luck next time.")
            print(f"The code was: {' '.join(str(n) for n in self.game.get_code_pattern())}")
            
    def _select_difficulty(self) -> Difficulty:
        """
        Prompt the user to select a difficulty level.
        
        Returns:
            Difficulty: The selected difficulty level
        """
        while True:
            print("\nSelect Difficulty:")
            print("1. Normal - 4 numbers (0-7), 10 attempts")
            print("2. Hard - 5 numbers (0-9), 8 attempts")
            choice = input("Select difficulty (1-2): ")
            
            selection_result = self.validator.validate_difficulty_selection(choice)
            if not selection_result.is_valid:
                print(selection_result.message)
                continue
                
            difficulty = Difficulty.NORMAL if choice == "1" else Difficulty.HARD
            logger.info("Difficulty selected: %s", difficulty)
            return difficulty