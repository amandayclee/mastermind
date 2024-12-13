import os
import sqlite3
import pytest

from src.repository.sqlite import SQLiteGameRepository
from src.services.exceptions.exceptions import GameNotFoundError, LoadError, SaveError


class TestSQLiteGameRepository:
    @pytest.fixture
    def db_path(self, tmp_path):
        """
        built in pytest temp_path
        """
        return str(tmp_path / "test_mastermind.db")
    
    @pytest.fixture
    def mock_repository(self, db_path):
        """
        Set up test db and add a temp stop point using yield,
        release the path after test is done
        """
        repo = SQLiteGameRepository(db_path)
        yield repo
        if os.path.exists(db_path):
            os.remove(db_path)
            
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
            
    def test_database_initialization(self, db_path):
        """
        Test database initialization
        """
        repository_for_this_test = SQLiteGameRepository(db_path)
        
        with sqlite3.connect(db_path) as conn:
            cursor = conn.execute("""
                SELECT name FROM sqlite_master 
                WHERE type='table' AND name='games'
            """)
            assert cursor.fetchone() is not None
    
    def test_database_persistence(self, db_path, sample_game_state):
        """
        Test game storage, sqlite has persistence
        """
        repo1 = SQLiteGameRepository(db_path)
        repo1.save_game(sample_game_state)
        
        repo2 = SQLiteGameRepository(db_path)
        loaded_state = repo2.load_game(sample_game_state.game_id)
        assert loaded_state.game_id == sample_game_state.game_id
        
    def test_save_error(self, mock_repository, sample_game_state):
        """
        Test save operation error
        """
        with pytest.raises(SaveError):
            sample_game_state.code_pattern = object()
            mock_repository.save_game(sample_game_state)
            
    def test_load_error(self, db_path, sample_game_state):
        """
        Test load operation error
        """
        repository_for_this_test = SQLiteGameRepository(db_path)
        repository_for_this_test.save_game(sample_game_state)
        
        with open(db_path, 'wb') as f:
            f.write(b'corrupted data')
            
        with pytest.raises(LoadError):
            repository_for_this_test.load_game(sample_game_state.game_id)
            
    def test_update_existing_game(self, mock_repository, sample_game_state):
        """
        Test updating an existing game
        """
        mock_repository.save_game(sample_game_state)
        
        sample_game_state.attempts += 1
        mock_repository.save_game(sample_game_state)
        
        loaded_state = mock_repository.load_game(sample_game_state.game_id)
        assert loaded_state.attempts == sample_game_state.attempts