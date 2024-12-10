from unittest.mock import Mock, patch
import pytest

from src.models.feedback import Feedback
from src.models.guess import Guess
from src.interface.game_interface import GameInterface

class TestGameInterface:
    @pytest.fixture
    def mock_game(self):
        game = Mock()
        game.code = [1, 2, 3, 4]
        game.is_active().return_value = True
        game.get_remaining_attempts.return_value = 10
        game.get_guess_records.return_value = []
        game.is_won.return_value = False
        game.code_pattern = [1, 2, 3, 4]
        
        return game
    
    @pytest.fixture
    def interface(self):
        return GameInterface()

    def test_set_game(self, mock_game, interface):
        interface.set_game(mock_game)
        
        assert interface.game == mock_game
        
    @patch('builtins.input', return_value='1234')
    def test_successful_guess(self, mock_input, mock_game, interface):
        mock_game.is_active.side_effect = [True, False]
        mock_game.validate_guess_input.return_value = [1, 2, 3, 4]
        guess_obj = Guess([1, 2, 3, 4])
        mock_game.create_guess.return_value = guess_obj
        mock_game.get_guess_records.return_value = [(guess_obj, Feedback(2, 1))]
        
        interface.set_game(mock_game)

        with patch('builtins.print'):
            interface.run_game()

        mock_game.validate_guess_input.assert_called_once_with('1234')
        mock_game.create_guess.assert_called_once_with([1, 2, 3, 4])
        mock_game.make_guess.assert_called_once_with(guess_obj)