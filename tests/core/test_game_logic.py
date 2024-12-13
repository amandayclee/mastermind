from unittest.mock import Mock
import pytest

from src.core.models.game_difficulty import Difficulty
from src.core.models.guess import Guess
from src.core.config.game_config import GameConfig
from src.core.game_logic import GameLogic
from src.services.exceptions.exceptions import GameInitError, GeneratorError

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
        """
        Test successful code pattern generation
        """
        expected_pattern = [1, 2, 3, 4]
        
        result = mock_game_logic.generate_code_pattern(mock_generator)
        
        assert result == expected_pattern
        mock_generator.generate.assert_called_once_with(mock_game_logic.config)
        
    def test_generate_code_pattern_failure(self, mock_game_logic, mock_generator):
        """
        Test handling of generator failure
        """
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
        """
        Test pattern count calculation for various inputs
        """
        result = mock_game_logic.calculate_pattern_counts(guess_numbers)
        assert result == expected_counts
        
    @pytest.mark.parametrize("guess_numbers,pattern,pattern_counts,expected_numbers,expected_positions", [
        # all correct
        ([1, 2, 3, 4], [1, 2, 3, 4], {1: 1, 2: 1, 3: 1, 4: 1}, 4, 4),
        
        # right number wrong position
        ([4, 3, 2, 1], [1, 2, 3, 4], {1: 1, 2: 1, 3: 1, 4: 1}, 4, 0),
        
        # partial right
        ([1, 2, 5, 6], [1, 2, 3, 4], {1: 1, 2: 1, 3: 1, 4: 1}, 2, 2),
        
        # all wrong
        ([5, 6, 7, 8], [1, 2, 3, 4], {1: 1, 2: 1, 3: 1, 4: 1}, 0, 0),
        
        # with duolicate number guess
        ([1, 1, 1, 1], [1, 2, 3, 4], {1: 1, 2: 1, 3: 1, 4: 1}, 1, 1),
        ([1, 1, 2, 2], [1, 2, 1, 2], {1: 2, 2: 2}, 4, 2),
        ([1, 1, 1, 2], [1, 2, 1, 1], {1: 3, 2: 1}, 4, 2),
    ])
    def test_check_guess_various_scenarios(self, mock_game_logic, 
        guess_numbers, pattern, pattern_counts, 
        expected_numbers, expected_positions):
        """
        Test various guessing scenarios including duplicates and partial matches
        """
        guess = Guess(guess_numbers)
        feedback = mock_game_logic.check_guess(guess, pattern_counts, pattern)
        
        assert feedback.numbers_correct == expected_numbers
        assert feedback.positions_correct == expected_positions
        
    @pytest.fixture(params=[Difficulty.NORMAL, Difficulty.HARD])
    def different_configs(self, request):
        return GameConfig(difficulty=request.param)
    
    def test_check_guess_with_different_configs(self, different_configs):
        """
        Test game logic with different configurations
        """
        game_logic = GameLogic(different_configs)
        pattern_length = different_configs.pattern_length
        
        pattern = list(range(pattern_length))
        pattern_counts = {i: 1 for i in range(pattern_length)}
        guess = Guess(pattern)
        
        feedback = game_logic.check_guess(guess, pattern_counts, pattern)
        
        assert feedback.numbers_correct == pattern_length
        assert feedback.positions_correct == pattern_length