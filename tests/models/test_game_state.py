from datetime import datetime
import pytest

from src.core.models.feedback import Feedback
from src.core.models.game_status import GameStatus
from src.core.models.guess import Guess
from src.core.models.game_state import GameState


class TestGameState:
    @pytest.fixture
    def sample_game_state(self, game_config):
        return GameState(
            game_id="test_game_123",
            code_pattern=[1, 2, 3, 4],
            status=GameStatus.IN_PROGRESS,
            attempts=1,
            guess_records=[(Guess([0, 0, 3, 4]), Feedback(2, 2))],  # One guess made with some correct numbers
            created_at=datetime(2024, 1, 1, 12, 0),
            updated_at=datetime(2024, 1, 1, 12, 5),
            config=game_config
        )

    def test_state_initialization(self, sample_game_state, game_config):
        assert sample_game_state.game_id == "test_game_123"
        assert sample_game_state.code_pattern == [1, 2, 3, 4]
        assert sample_game_state.status == GameStatus.IN_PROGRESS
        assert sample_game_state.attempts == 1
        assert len(sample_game_state.guess_records) == 1
        assert sample_game_state.guess_records[0][0].get_numbers() == [0, 0, 3, 4]
        assert sample_game_state.config == game_config
        
    def test_to_db_format(self, sample_game_state):
        db_data = sample_game_state.to_db_format()
        
        assert db_data["game_id"] == "test_game_123"
        assert db_data["code_pattern"] == [1, 2, 3, 4]
        assert db_data["status"] == "in_progress"
        assert db_data["attempts"] == 1
        
        guess_record = db_data["guess_records"][0]
        print(guess_record["guess"])
        assert guess_record["guess"] == [0, 0, 3, 4]
        assert guess_record["feedback"]["numbers_correct"] == 2
        assert guess_record["feedback"]["positions_correct"] == 2
        
        assert isinstance(db_data["created_at"], str)
        assert isinstance(db_data["updated_at"], str)
        
    def test_from_db_format(self, sample_game_state):
        db_data = sample_game_state.to_db_format()
        reconstructed = GameState.from_db_format(db_data)
        
        assert reconstructed.game_id == sample_game_state.game_id
        assert reconstructed.code_pattern == sample_game_state.code_pattern
        assert reconstructed.status == sample_game_state.status
        assert reconstructed.attempts == sample_game_state.attempts
        
        original_guess = sample_game_state.guess_records[0]
        reconstructed_guess = reconstructed.guess_records[0]
        
        assert reconstructed_guess[0].get_numbers() == original_guess[0].get_numbers()
        assert reconstructed_guess[1].numbers_correct == original_guess[1].numbers_correct
        assert reconstructed_guess[1].positions_correct == original_guess[1].positions_correct
    