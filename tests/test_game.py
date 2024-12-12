import pytest
from unittest.mock import Mock
from src.core.game.game import Game
from src.core.game.game_logic import GameLogic
from src.core.game.state_manager import StateManager
from src.models.guess import Guess
from src.models.feedback import Feedback
from src.utils.exceptions import GameInitError, GeneratorError, GuessError, InvalidLengthError, RangeError
from src.models.game_status import GameStatus


class TestGame:
    @pytest.fixture
    def mock_generator(self):
        generator = Mock()
        generator.generate.return_value = [1, 2, 3, 4]
        
        return generator
    
    @pytest.fixture
    def game(self, mock_generator):
        return Game(generator=mock_generator)
    
    def test_game_initialization(self, game, mock_generator):
        assert game.status == GameStatus.IN_PROGRESS
        assert game.attempts == 0
        assert len(game.guess_records) == 0
        assert game.code_pattern == [1, 2, 3, 4]
        assert isinstance(game.game_logic, GameLogic)
        assert isinstance(game.state_manager, StateManager)
        mock_generator.generate.assert_called_once()
        
    def test_load_game(self, game):
        guess = Guess([5, 5, 5, 5])
        game.make_guess(guess)
        
        reloaded_game = Game(game_id=game.game_id)
        assert reloaded_game.attempts == 1
        assert reloaded_game.code_pattern == game.code_pattern
        assert len(reloaded_game.guess_records) == 1
        assert reloaded_game.guess_records[0][0].get_numbers() == [5, 5, 5, 5]
        assert reloaded_game.status == game.status
        
    def test_make_guess_one_time_not_correct(self, game):
        guess = Guess([1, 5, 6, 7])
        game.make_guess(guess)
        history = game.get_guess_history()
        
        assert history[0][0].get_numbers() == [1, 5, 6, 7]
        assert isinstance(history[0][1], Feedback)
        
        assert game.attempts == 1
        assert len(game.guess_records) == 1
        assert game.status == GameStatus.IN_PROGRESS
        
    def test_make_guess_all_correct(self, game):
        guess = Guess([1, 2, 3, 4])
        game.make_guess(guess)
        history = game.get_guess_history()
        
        assert isinstance(history[0][1], Feedback)
        assert game.attempts == 1
        assert len(game.guess_records) == 1
        assert game.status == GameStatus.WON
        
        reloaded_game = Game(game_id=game.game_id)
        assert reloaded_game.status == GameStatus.WON
        
    def test_make_guess_max_attempts(self, game):
        wrong_guess = Guess([5, 5, 5, 5])
        for _ in range(game.config.max_attempts):
            game.make_guess(wrong_guess)
        
        assert game.attempts == 10
        assert len(game.guess_records) == 10
        assert game.status == GameStatus.LOST
        assert game.get_remaining_attempts() == 0

        reloaded_game = Game(game_id=game.game_id)
        assert reloaded_game.status == GameStatus.LOST
        
        
    @pytest.mark.parametrize("invalid_input,expected_exception", [
        ("", GuessError),
        ("abc", GuessError),
        ("123", InvalidLengthError),
        ("12345", InvalidLengthError),
        ("8888", RangeError)
    ])
    def test_validate_guess_input_invalid(self, game, invalid_input, expected_exception):
        with pytest.raises(expected_exception):
            game.validate_guess_input(invalid_input)
    
    
    def test_get_guess_history(self, game):
        guess1 = Guess([1, 1, 1, 1])
        guess2 = Guess([2, 2, 2, 2])
        
        game.make_guess(guess1)
        game.make_guess(guess2)
        
        history = game.get_guess_history()
        assert len(history) == 2
        assert isinstance(history[0][0], Guess)
        assert isinstance(history[0][1], Feedback)

    def test_get_remaining_attempts(self, game):
        initial_remaining = game.get_remaining_attempts()
        game.make_guess(Guess([5, 5, 5, 5]))
        assert game.get_remaining_attempts() == initial_remaining - 1
    
    def test_game_status_transition(self, game):
        assert game.status == GameStatus.IN_PROGRESS
        
        guess = Guess([1, 2, 3, 4])
        game.make_guess(guess)
        assert game.status == GameStatus.WON
    
        
    # def test_generate_code_pattern_error_handling(self):
    #     mock_generator = Mock()
    #     mock_generator.generate.side_effect = GeneratorError("API error")
        
    #     with pytest.raises(GameInitError) as excinfo:
    #         Game(generator=mock_generator)
    #     assert "Failed to initialize game" in str(excinfo.value)


    # def test_pattern_count_calculation(self, game):
    #     mock_generator = Mock()
    #     mock_generator.generate.return_value = [1, 1, 2, 3]
    #     game = Game(generator=mock_generator)
        
    #     assert game.pattern_count == {1: 2, 2: 1, 3: 1}
        
    # @pytest.mark.parametrize("guess_numbers,expected_numbers,expected_locations", [
    #     ([1, 1, 2, 3], 4, 4),
    #     ([1, 1, 3, 2], 4, 2),
    #     ([1, 2, 2, 3], 3, 3),
    #     ([4, 4, 4, 4], 0, 0),
    # ])
    # def test_check_guess_with_duplicates(self, guess_numbers, expected_numbers, expected_locations):
    #     mock_generator = Mock()
    #     mock_generator.generate.return_value = [1, 1, 2, 3]
    #     game = Game(generator=mock_generator)
        
    #     correct_number, correct_location = game._check_guess(Guess(guess_numbers))
        
    #     assert correct_number == expected_numbers
    #     assert correct_location == expected_locations
        