from datetime import datetime
from src.models.exceptions import GuessError, InvalidLengthError, RangeError
from src.models.guess import Guess
from src.models.player import Player


class GameInterface:
    def __init__(self):
        self.game = None
        
    def set_game(self, game):
        self.game = game
    
    def run_game(self):
        print("Welcome to the mastermind game!")
        
        while self.game.is_active():
            self._display_game_state()
            guess_input = input("What's your guess? ")
            
            try:
                valid_numbers = self.game.validate_guess_input(guess_input)
                guess = self.game.create_guess(valid_numbers)
                self.game.make_guess(guess)
            except (GuessError, InvalidLengthError, RangeError) as e:
                print(f"{e.message}")
                continue
                            
        self._display_game_result()
            
    def _display_game_state(self):
        print(f"Code Pattern: {self.game.code_pattern}")
        
        guess_records = self.game.get_guess_history()
        attempts_left = self.game.get_remaining_attempts()
        
        if not guess_records:
            print("It's time for your first guess!")
            print(f"You have {attempts_left} attempts remaining.")
            return
        
        print(f"You've played {len(guess_records)} rounds!")
        for record in guess_records:
            guess_display = " ".join(str(n) for n in record[0].get_numbers())
            feedback = record[1]
            print(f"Player guesses \"{guess_display}\", {feedback}")
            
        print(f"\nYou have {attempts_left} attempts remaining.")
            
    def _display_game_result(self):
        if self.game.is_won():
            print("Congrats! You win the game!")
        else:
            print("Game Over! Better luck next time.")
            print(f"The code was: {' '.join(str(n) for n in self.game.code_pattern)}")