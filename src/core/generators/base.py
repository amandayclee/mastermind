from abc import ABC, abstractmethod
from typing import List
from src.config.game_config import GameConfig


class NumberGenerator(ABC):
    @abstractmethod
    def generate(self, config: GameConfig) -> List[int]:
        pass