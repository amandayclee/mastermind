import pytest
from unittest.mock import Mock
from src.core.game import Game
from src.core.game_logic import GameLogic
from src.core.state_manager import StateManager
from src.core.models.guess import Guess
from src.core.models.feedback import Feedback
from src.core.models.game_status import GameStatus


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
        """
        Test loading existing game
        """
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
        """
        Test making an incorrect guess
        """
        guess = Guess([1, 5, 6, 7])
        game.make_guess(guess)
        history = game.get_guess_history()
        
        assert history[0][0].get_numbers() == [1, 5, 6, 7]
        assert isinstance(history[0][1], Feedback)
        
        assert game.attempts == 1
        assert len(game.guess_records) == 1
        assert game.status == GameStatus.IN_PROGRESS
        
    def test_make_guess_all_correct(self, game):
        """
        Test making a winning guess
        """
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
        """
        Test reaching maximum attempts
        """
        wrong_guess = Guess([5, 5, 5, 5])
        for _ in range(game.config.max_attempts):
            game.make_guess(wrong_guess)
        
        assert game.attempts == 10
        assert len(game.guess_records) == 10
        assert game.status == GameStatus.LOST
        assert game.get_remaining_attempts() == 0

        reloaded_game = Game(game_id=game.game_id)
        assert reloaded_game.status == GameStatus.LOST
        
        
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
        
    def test_get_status(self, game):
        assert game.get_status() == GameStatus.IN_PROGRESS
        
        guess = Guess([1, 2, 3, 4])
        game.make_guess(guess)
        
        assert game.get_status() == GameStatus.WON

    def test_get_code_pattern(self, game):        
        assert game.get_code_pattern() == game.code_pattern
