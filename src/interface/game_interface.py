import logging
from src.models.game_status import GameStatus
from src.core.game.game import Game
from src.utils.exceptions import GuessError, InvalidLengthError, RangeError

logger = logging.getLogger(__name__)

class GameInterface:
    def __init__(self) -> None:
        self.game = None
        
    def set_game(self, game: Game) -> None:
        self.game = game
        print(f"\nYour game ID is: {self.game.game_id}")
        print("Keep this ID if you want to continue this game later!")
    
    def run_game(self) -> None:
        print("Type 'exit' to return to main menu")
        print("Type 'id' to see your game ID")
        
        while self.game.get_status() == GameStatus.IN_PROGRESS:
            self._display_game_state()
            guess_input = input("Please enter 4 numbers with each number is between 0 and 7:\n")
            
            if guess_input == 'id':
                print(f"\nYour game ID is: {self.game.game_id}")
                continue
            elif guess_input == 'exit':
                print(f"\nExiting game. Your game ID is: {self.game.game_id}")
                print("Use this ID to continue your game later!")
                return
            
            try:
                valid_guess = self.game.validate_guess_input(guess_input)
                self.game.make_guess(valid_guess)
            except (GuessError, InvalidLengthError, RangeError) as e:
                print(f"{e.get_message()}")
                continue
                            
        self._display_game_result()
            
    def _display_game_state(self) -> None:
        # print(f"Code Pattern: {self.game.code_pattern}")
        
        guess_records = self.game.get_guess_history() 
        attempts_left = self.game.get_remaining_attempts()
        
        if guess_records:
            print("\n====== Previous Guesses ======")
        
        for record in guess_records:
            print(f"Player guesses \"{record[0]}\", {record[1]}")

            
        print(f"\nAttempts remaining: {attempts_left}\n")
            
    def _display_game_result(self) -> None:
        print("\n========= Game Over =========")
        if self.game.get_status() == GameStatus.WON:
            print("Congrats! You win the game!")
        else:
            print("Game Over! Better luck next time.")
            print(f"The code was: {' '.join(str(n) for n in self.game.get_code_pattern())}")