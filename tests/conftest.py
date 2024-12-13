from datetime import datetime
from unittest.mock import Mock
import pytest
from src.core.models.game_state import GameState
from src.core.models.game_status import GameStatus
from src.repository.base import GameRepository
from src.core.models.guess import Guess
from src.core.config.game_config import GameConfig

@pytest.fixture
def game_config():
    return GameConfig()

@pytest.fixture
def sample_guess():
    return Guess([1, 2, 3, 4])

@pytest.fixture
def mock_repository():
    return Mock(spec=GameRepository)

@pytest.fixture
def sample_game_state():
    """Create a sample game state for testing"""
    return GameState(
        game_id="test-123",
        code_pattern=[1, 2, 3, 4],
        status=GameStatus.IN_PROGRESS,
        attempts=2,
        guess_records=[],
        created_at=datetime.now(),
        updated_at=datetime.now(),
        config=GameConfig()
    )