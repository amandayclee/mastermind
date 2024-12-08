from datetime import datetime
import requests
from src.models.guess import Guess
from src.models.feedback import Feedback
from src.config.game_config import GameConfig
from src.models.exceptions import GuessError, InvalidLengthError, RangeError

class Game:
    def __init__(self):
        self.config = GameConfig()
        self._is_active = True
        self._is_won = False
        self.pattern_count = {}
        self.code_pattern = self._generate_code_pattern()
        self.attempts = 0
        self.guess_records = []
        
    def is_active(self):
        return self._is_active
    
    def is_won(self):
        return self._is_won

    def get_remaining_attempts(self):
        return self.config.max_attempts - self.attempts
    
    def get_guess_history(self):
        return self.guess_records.copy()
    
    def validate_guess_input(self, guess_input):
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

    def create_guess(self, numbers):
        """Create a valid Guess object from validated numbers"""
        return Guess(numbers, datetime.today().strftime('%Y-%m-%d %H:%M:%S'))

    def make_guess(self, guess):
        """Handle a guess and update game status"""
        correct_number = self._check_number(guess)
        correct_location = self._check_location(guess)
        
        feedback = Feedback(correct_number, correct_location)
        record = [guess, feedback]
        
        self.guess_records.append(record)
        
        self.attempts += 1
        
        self._update_game_state(correct_number, correct_location)
        
        return feedback
    
    def _generate_code_pattern(self):
        while True:
            try:
                api_params = self.config.get_api_params()
                api_link = self.config.api_base_url + "?" + "&".join(f"{key}={value}" for key, value in api_params.items())
                
                response = requests.get(api_link)
                response.raise_for_status()
                code_pattern = [int(_) for _ in response.text.strip("\n").split("\t")]
                self._calculate_pattern_counts(code_pattern)
                return code_pattern
            
            except requests.exceptions.RequestException as e:
                print(f"{e}, API request failed.")
        
    def _calculate_pattern_counts(self, code_pattern):
        for num in code_pattern:
            self.pattern_count[num] = self.pattern_count.get(num, 0) + 1
        
        print(self.pattern_count)
              
    def _update_game_state(self, correct_number, correct_location):
        """Update game state after make a guess"""
        if correct_number == len(self.code_pattern) and correct_location == len(self.code_pattern):
            self._is_won = True
            self._is_active = False
        elif self.attempts >= self.config.max_attempts:
            self._is_active = False
        
    def _check_number(self, player_guess):
        """Check correct number in a guess"""
        player_guess = player_guess.get_guess()
        correct_number = 0
        pattern_count_copy = self.pattern_count.copy()
        
        for i in range(len(player_guess)):
            if player_guess[i] in self.code_pattern and pattern_count_copy[player_guess[i]] != 0:
                correct_number += 1
                pattern_count_copy[player_guess[i]] -= 1
        
        return correct_number
    
    def _check_location(self, player_guess):
        """Check correct location in a guess"""
        player_guess = player_guess.get_guess()
        correct_location = 0
        
        for i in range(len(player_guess)):
            if player_guess[i] == self.code_pattern[i]:
                correct_location += 1
        
        return correct_location