from unittest.mock import Mock
import pytest

from src.core.game.game import Game
from src.models.guess import Guess
from src.models.game_status import GameStatus

class TestGameStatus:
    @pytest.fixture
    def mock_generator(self):
        generator = Mock()
        generator.generate.return_value = [1, 2, 3, 4]
        
        return generator

    @pytest.fixture
    def game(self, mock_generator):
        return Game(generator=mock_generator)


    @pytest.mark.parametrize("attempts,expected_status", [
        (0, GameStatus.IN_PROGRESS),
        (9, GameStatus.IN_PROGRESS),
        (10, GameStatus.LOST)
    ])
    def test_game_status_based_on_attempts(self, game, attempts, expected_status):
        wrong_guess = Guess([5, 5, 5, 5])
        for _ in range(attempts):
            game.make_guess(wrong_guess)
        assert game.status == expected_status