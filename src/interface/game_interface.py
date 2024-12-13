import logging
from src.core.repository.sqlite import SQLiteGameRepository
from src.core.repository.base import GameRepository
from src.models.game_status import GameStatus
from src.core.game.game import Game
from src.utils.exceptions import GameNotFoundError, GuessError, InvalidLengthError, RangeError

logger = logging.getLogger(__name__)

class GameInterface:
    def __init__(self, repository: GameRepository = SQLiteGameRepository()) -> None:
        """
        Initialize a new game interface.
        
        Args:
            game (Game): Reference to the current game instance being played
            repository (GameRepository): Repository for game state persistence
        """
        self.game = None
        self.repository = repository
        
    def start_menu(self) -> None:
        """
        Start the main menu loop.
        
        Displays the main menu and handles user navigation including:
        - Starting new games
        - Loading existing games
        - Exiting the program
        
        The menu continues to loop until the user chooses to exit.
        """
        while True:
            print("\n****** Mastermind ******")
            print("1. New Game")
            print("2. Load Game")
            print("3. Exit Program")
            choice = input("Select an option (1-3): ")
            
            if choice == "1":
                self.game = Game(repository=self.repository)
                print(f"\nYour game ID is: {self.game.game_id}")
                print("Keep this ID if you want to continue this game later!\n")
                self.run_game()
            elif choice == "2":
                while True:
                        game_id = input("Enter your game ID (or 'exit' to return to menu): ").strip()
                        
                        if game_id.lower() == 'exit':
                            print("Returning to main menu...\n")
                            break
                            
                        if not game_id:
                            print("Game ID cannot be empty. Please enter a valid game ID.\n")
                            continue
                            
                        try:
                            self.game = Game(repository=self.repository, game_id=game_id)
                            self.run_game()
                            break
                            
                        except GameNotFoundError:
                            print(f"Game with ID '{game_id}' not found.\n")
                            print("Please try again or type 'exit' to return to the main menu.\n")
            elif choice == "3":
                print("Thanks for playing!")
                break
            else:
                print("Invalid choice. Please select 1, 2, or 3")
        
    
    def run_game(self) -> None:
        """
        Run the main game loop.
        """
        print("Type 'exit' to return to main menu")
        print("Type 'id' to see your game ID")
        
        while self.game.get_status() == GameStatus.IN_PROGRESS:
            self._display_game_state()
            guess_input = input(f"Please enter {self.game.config.pattern_length} numbers with each number is between {self.game.config.min_number} and {self.game.config.max_number}:\n")
            
            if guess_input == 'id':
                print(f"\nYour game ID is: {self.game.game_id}")
                continue
            elif guess_input == 'exit':
                print(f"\nExiting game. Your game ID is: {self.game.game_id}")
                print("Use this ID to continue your game later!")
                return
            
            self.process_user_input(guess_input)
                            
        self._display_game_result()
            
    def process_user_input(self, guess_input: str) -> None:
        """
        Process and validate user's guess input.
        
        Args:
            guess_input (str): The user's input string containing their guess
            
        The method handles validation and error display for:
        - Input format
        - Number range
        - Input length
        """
        try:
            valid_guess = self.game.validate_guess_input(guess_input)
            self.game.make_guess(valid_guess)
        except (GuessError, InvalidLengthError, RangeError) as e:
            print(f"{e.get_message()}")
            
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
            
    def _display_game_result(self) -> None:
        """
        Display the final game result.
        
        Shows:
        - Win/loss message
        - The secret code pattern (if the player lost)
        """
        print("\n========= Game Over =========")
        if self.game.get_status() == GameStatus.WON:
            print("Congrats! You win the game!")
        else:
            print("Game Over! Better luck next time.")
            print(f"The code was: {' '.join(str(n) for n in self.game.get_code_pattern())}")