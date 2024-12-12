from unittest.mock import Mock
import pytest

from src.models.guess import Guess
from src.config.game_config import GameConfig
from src.core.game.game_logic import GameLogic
from src.utils.exceptions import GameInitError, GeneratorError

class TestGameLogic:
    @pytest.fixture
    def mock_game_logic(self, game_config):
        return GameLogic(game_config)
    
    @pytest.fixture
    def mock_generator(self):
        generator = Mock()
        generator.generate.return_value = [1, 2, 3, 4]
        return generator
    
    def test_generate_code_pattern_success(self, mock_game_logic, mock_generator):
        expected_pattern = [1, 2, 3, 4]
        
        result = mock_game_logic.generate_code_pattern(mock_generator)
        
        assert result == expected_pattern
        mock_generator.generate.assert_called_once_with(mock_game_logic.config)
        
    def test_generate_code_pattern_failure(self, mock_game_logic, mock_generator):
        mock_generator.generate.side_effect = GeneratorError("API Error")
        
        with pytest.raises(GameInitError) as exc_info:
            mock_game_logic.generate_code_pattern(mock_generator)
        assert "Failed to initialize game" in str(exc_info.value)
        
    @pytest.mark.parametrize("guess_numbers,expected_counts", [
        ([1, 2, 3, 4], {1: 1, 2: 1, 3: 1, 4: 1}),
        ([1, 1, 2, 2], {1: 2, 2: 2}),
        ([0, 0, 0, 0], {0: 4}),
    ])
    def test_calculate_pattern_counts(self, mock_game_logic, guess_numbers, expected_counts):
        result = mock_game_logic.calculate_pattern_counts(guess_numbers)
        assert result == expected_counts
        
    def test_check_guess_all_correct(self, mock_game_logic):
        pattern = [1, 2, 3, 4]
        pattern_counts = {1: 1, 2: 1, 3: 1, 4: 1}
        guess = Guess([1, 2, 3, 4])
        
        feedback = mock_game_logic.check_guess(guess, pattern_counts, pattern)
        
        assert feedback.numbers_correct == 4
        assert feedback.positions_correct == 4