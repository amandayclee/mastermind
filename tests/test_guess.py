import pytest
from datetime import datetime
from models.guess import Guess

class TestGuess:
    def test_guess_initialization(self):
        guess_string = "1234"
        timestamp = "2024-12-07 15:58:00"
        guess = Guess(guess_string, timestamp)
        
        assert guess.guess_array == ['1', '2', '3', '4']
        assert guess.timestamp == timestamp
        
    def test_guess_get(self):
        guess_string = "5678"
        timestamp = "2024-12-07 15:58:00"
        guess = Guess(guess_string, timestamp)
        
        result = guess.get_guess()
        
        assert isinstance(result, list)
        assert result == ['5', '6', '7', '8']
        
    def test_guess_timestamp(self):
        guess_string = "1234"
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        guess = Guess(guess_string, current_time)
        
        assert guess.timestamp == current_time