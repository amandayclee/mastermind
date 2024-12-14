from datetime import datetime
from unittest.mock import Mock, call, patch
import pytest

from src.core.models.game_difficulty import Difficulty
from src.core.models.game_status import GameStatus
from src.core.state_manager import StateManager
from src.interface.game_interface import GameInterface
from src.services.exceptions.exceptions import GameNotFoundError

class TestGameInterface:
    @pytest.fixture
    def mock_game(self, game_config):
        game = Mock()
        game.config = game_config
        game.game_id="test-123"
        game.code_pattern=[1, 2, 3, 4]
        game.get_remaining_attempts.return_value = 2
        game.get_guess_history.return_value = []
        game.status = GameStatus.IN_PROGRESS
        game.created_at = datetime.now()
        game.updated_at = datetime.now()
        
        return game
    
    @pytest.fixture
    def mock_interface(self, mock_repository):
        return GameInterface(repository=mock_repository)

    @patch('builtins.input')
    @patch('builtins.print')
    def test_start_menu_new_game(self, mock_print, mock_input, mock_interface, mock_game):
        """Test starting a new game from menu."""
        mock_input.side_effect = ["1", "1", "exit", "3"]
        with patch('src.core.game.Game', return_value=mock_game):
            mock_interface.start_menu()
            
        assert mock_print.mock_calls[:4] == [
            call("\n****** Mastermind ******"),
            call("1. New Game"),
            call("2. Load Game"),
            call("3. Exit Program")
        ]
    
    @patch('builtins.input')
    @patch('builtins.print')
    def test_start_menu_invalid_choice(self, mock_print, mock_input, mock_interface):
        """
        Test invalid menu choice
        """
        mock_input.side_effect = ["4", "3"]
        mock_interface.start_menu()
        mock_print.assert_any_call("Invalid choice. Please select 1, 2, or 3")

    @patch('builtins.input')
    @patch('builtins.print')
    def test_load_game_exit(self, mock_print, mock_input, mock_interface):
        """
        Test exiting from load game menu
        """
        mock_input.side_effect = ["2", "exit", "3"]
        mock_interface.start_menu()
        mock_print.assert_any_call("Returning to main menu...\n")
        
    @patch('builtins.input')
    @patch('builtins.print')
    def test_load_game_invalid_id(self, mock_print, mock_input, mock_interface):
        """
        Test loading game with invalid ID format
        """
        mock_input.side_effect = ["2", "wrong-id", "exit", "3"]
        mock_interface.validator.validate_game_id = Mock(return_value=Mock(is_valid=False, message="Invalid ID format"))
        mock_interface.start_menu()
        mock_print.assert_any_call("Invalid ID format")

    @patch('builtins.input')
    @patch('builtins.print')
    def test_load_game_exit(self, mock_print, mock_input, mock_interface):
        """
        Test exiting from load game menu
        """
        mock_input.side_effect = ["2", "exit", "3"]
        mock_interface.start_menu()
        mock_print.assert_any_call("Returning to main menu...\n")
        
        
    @patch('builtins.input')
    @patch('builtins.print')
    def test_load_game_invalid_id(self, mock_print, mock_input, mock_interface):
        """
        Test loading game with invalid ID format
        """
        mock_input.side_effect = ["2", "invalid-id", "exit", "3"]
        mock_interface.validator.validate_game_id = Mock(return_value=Mock(is_valid=False, message="Invalid ID format"))
        mock_interface.start_menu()
        mock_print.assert_any_call("Invalid ID format")
        
    @patch('builtins.input')
    @patch('builtins.print')
    def test_load_game_not_found(self, mock_print, mock_input, mock_interface):
        """
        Test loading non-existent game
        """
        mock_input.side_effect = ["2", "wrong-uuid", "exit", "3"]
        mock_interface.validator.validate_game_id = Mock(return_value=Mock(is_valid=True)) # return ValidationResult
        
        mock_interface.repository.load_game.side_effect = GameNotFoundError("wrong-uuid")
        with patch('src.core.game.Game', side_effect=GameNotFoundError("valid-id")):
            mock_interface.start_menu()
            
        mock_print.assert_any_call("Game with ID 'wrong-uuid' not found.\n")
        
    @patch('builtins.input')
    @patch('builtins.print')
    def test_process_guess_input_invalid_format(self, mock_print, mock_input, mock_interface, mock_game):
        """
        Test invalid guess format
        """
        mock_interface.validator.validate_guess_input = Mock(return_value=Mock(is_valid=False, message="Invalid format"))
        mock_interface.game = mock_game
        mock_interface.process_guess_input("abc")
        mock_print.assert_called_with("Invalid format")
        
    @patch('builtins.input')
    @patch('builtins.print')
    def test_process_guess_input_out_of_range(self, mock_print, mock_input, mock_interface, mock_game):
        """
        Test guess numbers out of valid range
        """
        mock_interface.validator.validate_guess_input = Mock(return_value=Mock(is_valid=True))
        mock_interface.validator.parse_guess_input = Mock(return_value=[9, 9, 9, 9])
        mock_interface.validator.validate_number_range = Mock(return_value=Mock(is_valid=False, message="Numbers out of range"))
        mock_interface.game = mock_game
        mock_interface.process_guess_input("9999")
        mock_print.assert_called_with("Numbers out of range")
        
    @patch('builtins.input')
    @patch('builtins.print')
    def test_display_game_result_win(self, mock_print, mock_input, mock_interface, mock_game):
        """
        Test displaying win game result
        """
        mock_game.get_status.return_value = GameStatus.WON
        mock_interface.game = mock_game
        mock_interface._display_game_result()
        mock_print.assert_any_call("Congrats! You win the game!")