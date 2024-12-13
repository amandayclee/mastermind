from datetime import datetime
from unittest.mock import Mock, call, patch
import pytest

from src.core.models.game_status import GameStatus
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
    

        game.status = GameStatus.IN_PROGRESS
        game.created_at = datetime.now()
        
        return game
    
    @pytest.fixture
    def mock_interface(self, mock_repository):
        return GameInterface(repository=mock_repository)

    @patch('builtins.input')
    @patch('builtins.print')
    def test_start_menu_new_game(self, mock_print, mock_input, mock_interface, mock_game):
        """Test starting a new game from menu."""
        mock_input.side_effect = ['1', 'exit', '3']
        with patch('src.core.game.Game', return_value=mock_game):
            mock_interface.start_menu()
            
        assert mock_print.mock_calls[:4] == [
            call("\n****** Mastermind ******"),
            call("1. New Game"),
            call("2. Load Game"),
            call("3. Exit Program")
        ]
        
        assert mock_print.mock_calls[5] == call("Keep this ID if you want to continue this game later!\n")
        assert mock_print.mock_calls[6] == call("Type 'exit' to return to main menu")
        assert mock_print.mock_calls[7] == call("Type 'id' to see your game ID")
        assert mock_print.mock_calls[8] == call("\nAttempts remaining: 10\n")