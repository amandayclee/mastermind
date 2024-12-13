import pytest
from src.repository.memory import InMemoryGameRepository
from src.services.exceptions.exceptions import GameNotFoundError


class TestInMemoryRepository:
    @pytest.fixture
    def mock_repository(self):
        return InMemoryGameRepository()
    
    def test_save_and_load_game(self, mock_repository, sample_game_state):
        """
        Test basic save and load
        """
        mock_repository.save_game(sample_game_state)
        loaded_state = mock_repository.load_game(sample_game_state.game_id)
        
        assert loaded_state.game_id == sample_game_state.game_id
        assert loaded_state.code_pattern == sample_game_state.code_pattern
        assert loaded_state.status == sample_game_state.status
        assert loaded_state.attempts == sample_game_state.attempts
        
    def test_load_non_existent_game(self, mock_repository):
        """
        Test error throw for load non-existent game
        """
        with pytest.raises(GameNotFoundError):
            mock_repository.load_game("wrong_id")
            
    def test_update_existing_game(self, mock_repository, sample_game_state):
        """
        Test update existing game
        """
        mock_repository.save_game(sample_game_state)
        
        sample_game_state.attempts += 1
        mock_repository.save_game(sample_game_state)
        
        loaded_state = mock_repository.load_game(sample_game_state.game_id)
        assert loaded_state.attempts == sample_game_state.attempts
        
    def test_memory_persistence(self, mock_repository, sample_game_state):
        """
        Test game storage, in memory doesn't have persistence
        """
        mock_repository.save_game(sample_game_state)
        assert sample_game_state.game_id in mock_repository._store
        
        new_repository = InMemoryGameRepository()
        with pytest.raises(GameNotFoundError):
            new_repository.load_game("wrong_id")