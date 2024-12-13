import pytest
from src.core.models.feedback import Feedback


def test_basic_initialization():
    feedback = Feedback(2, 1)
    assert feedback.numbers_correct == 2
    assert feedback.positions_correct == 1

@pytest.mark.parametrize("numbers,positions,code_length,expected", [
    (4, 4, 4, True),   # Perfect match
    (4, 3, 4, False),  # All numbers correct but one position wrong
    (4, 2, 4, False),  # All numbers correct but two positions wrong
    (2, 2, 4, False),  # Partial correct
    (0, 0, 4, False),  # All incorrect
])
def test_winning_guess(numbers, positions, code_length, expected):
    feedback = Feedback(numbers, positions)
    assert feedback.is_winning_guess(code_length) == expected
    
@pytest.mark.parametrize("numbers,positions,expected_str", [
    (2, 1, "2 correct numbers and 1 correct positions"),
    (0, 0, "0 correct numbers and 0 correct positions"),
    (4, 4, "4 correct numbers and 4 correct positions"),
])
def test_string_representation(numbers, positions, expected_str):
    feedback = Feedback(numbers, positions)
    assert str(feedback) == expected_str
    
