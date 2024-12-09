import pytest
from src.models.guess import Guess

class TestGuess:
    def test_guess_initialization(self):
        numbers = [1, 2, 3, 4]
        guess = Guess(numbers)
        assert guess.numbers == numbers
            
    def test_string_representation(self):
        numbers = [5, 6, 7, 0]
        guess = Guess(numbers)
        assert str(guess) == "5 6 7 0"