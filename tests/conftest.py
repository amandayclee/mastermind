import pytest
from src.config.game_config import GameConfig

@pytest.fixture
def game_config():
    return GameConfig()