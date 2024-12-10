from src.core.game import Game
from src.utils.exceptions import GuessError, InvalidLengthError, RangeError


class GameInterface:
    def __init__(self) -> None:
        self.game = None
        
    def set_game(self, game: Game) -> None:
        """"""
        self.game = game
    
    def run_game(self) -> None:
        print("****** Welcome to Mastermind ******")
        print("Type 'exit' if you want to quit")
        
        while self.game.is_active():
            self._display_game_state()
            guess_input = input("Please enter 4 numbers with each number is between 0 and 7:\n")
            
            if guess_input == 'exit':
                return
            
            try:
                valid_numbers = self.game.validate_guess_input(guess_input)
                guess = self.game.create_guess(valid_numbers)
                self.game.make_guess(guess)
            except (GuessError, InvalidLengthError, RangeError) as e:
                print(f"{e.get_message()}")
                continue
                            
        self._display_game_result()
            
    def _display_game_state(self) -> None:
        # print(f"Code Pattern: {self.game.code_pattern}")
        
        guess_records = self.game.guess_records
        attempts_left = self.game.get_remaining_attempts()
        
        if guess_records:
            print("\n====== Previous Guesses ======")
        
        for record in guess_records:
            print(f"Player guesses \"{record[0]}\", {record[1]}")

            
        print(f"\nAttempts remaining: {attempts_left}\n")
            
    def _display_game_result(self) -> None:
        print("\n========= Game Over =========")
        if self.game.is_won():
            print("Congrats! You win the game!")
        else:
            print("Game Over! Better luck next time.")
            print(f"The code was: {' '.join(str(n) for n in self.game.code_pattern)}")