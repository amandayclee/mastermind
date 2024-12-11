from datetime import datetime
from unittest.mock import Mock, patch
import pytest

from src.models.game_status import GameStatus
from src.models.feedback import Feedback
from src.models.guess import Guess
from src.interface.game_interface import GameInterface

class TestGameInterface:
    @pytest.fixture
    def mock_game(self, game_config):
        game = Mock()
        game.config = game_config
        
        game.code_pattern = [5, 6, 7, 0]

        game.is_active().return_value = True
        game.get_remaining_attempts.return_value = 10
        game.get_guess_history.return_value = []
        game.is_won.return_value = False
    
        
        game.game_id = "test-game-id"
        game.status = GameStatus.IN_PROGRESS
        game.created_at = datetime.now()
        
        return game
    
    @pytest.fixture
    def interface(self):
        return GameInterface()

    @patch('builtins.print') 
    def test_set_game(self, mock_print, mock_game, interface):
        interface.set_game(mock_game)
        
        assert interface.game == mock_game
        mock_print.assert_any_call("\nYour game ID is: test-game-id")
    
    @patch('builtins.print')
    @patch('builtins.input', side_effect=['1234', 'exit'])
    def test_successful_wrong_guess_and_exit(self, mock_input, mock_print, mock_game, interface, sample_guess):
        mock_game.is_active.side_effect = [True, True]
        mock_game.validate_guess_input.return_value = sample_guess.get_numbers()
        mock_game.create_guess.return_value = sample_guess
        
        mock_game.get_guess_history.return_value = [(sample_guess, Feedback(0, 0))]
        
        interface.set_game(mock_game)
        interface.run_game()

        mock_game.validate_guess_input.assert_called_once_with('1234')
        mock_game.create_guess.assert_called_once_with(sample_guess.get_numbers())
        mock_game.make_guess.assert_called_once_with(sample_guess)
        
        assert mock_game.status == GameStatus.IN_PROGRESS