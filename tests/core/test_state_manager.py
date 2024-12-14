from unittest.mock import Mock
import pytest

from src.core.models.game_status import GameStatus
from src.core.state_manager import StateManager
from src.services.exceptions.exceptions import GameNotFoundError


class TestStateManager:
    @pytest.fixture
    def mock_state_manager(self, mock_repository):
        return StateManager(mock_repository)
    
    def test_save_state_success(self, mock_state_manager, mock_repository, sample_game_state):
        """
        Test successful game state saving
        """
        mock_state_manager.save_state(sample_game_state)
         
        mock_repository.save_game.assert_called_once_with(sample_game_state)
        
    def test_load_game_success(self, mock_state_manager, mock_repository, sample_game_state):
        """
        Test successful game state loading
        """
        mock_repository.load_game.return_value = sample_game_state
        loaded_state = mock_state_manager.load_state("test-123")
        
        mock_repository.load_game.assert_called_once_with("test-123")
        assert loaded_state == sample_game_state
        assert loaded_state.game_id == "test-123"
        assert loaded_state.status == GameStatus.IN_PROGRESS
        assert loaded_state.attempts == 2
        
    def test_load_state_not_found(self, mock_state_manager, mock_repository):
        """
        Test loading non-existent game state
        """
        mock_repository.load_game.side_effect = GameNotFoundError("wrong_id")
    
        with pytest.raises(GameNotFoundError):
            mock_state_manager.load_state("wrong_id")

        mock_repository.load_game.assert_called_once_with("wrong_id")
        
    def test_save_state_with_different_status(self, mock_state_manager, mock_repository, sample_game_state):
        sample_game_state.status = GameStatus.WON
        mock_state_manager.save_state(sample_game_state)
        mock_repository.save_game.assert_called_with(sample_game_state)
        
        sample_game_state.status = GameStatus.LOST
        mock_state_manager.save_state(sample_game_state)
        mock_repository.save_game.assert_called_with(sample_game_state)
        
    def test_state_manager_initialization(self, mock_repository):
        """
        Test state manager initialization with repository
        """
        manager = StateManager(mock_repository)
        assert manager.repository == mock_repository