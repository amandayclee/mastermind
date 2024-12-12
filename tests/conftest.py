from unittest.mock import Mock
import pytest
from src.core.repository.base import GameRepository
from src.models.guess import Guess
from src.config.game_config import GameConfig

@pytest.fixture
def game_config():
    return GameConfig()

@pytest.fixture
def sample_guess():
    return Guess([1, 2, 3, 4])

@pytest.fixture
def mock_repository():
    return Mock(spec=GameRepository)