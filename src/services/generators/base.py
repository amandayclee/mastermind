from abc import ABC, abstractmethod
from typing import List
from src.core.config.game_config import GameConfig


class NumberGenerator(ABC):
    """
    Abstract base class for number generation strategies.
    """
    @abstractmethod
    def generate(self, config: GameConfig) -> List[int]:
        """
        Generate a list of random numbers according to the game configuration.
        
        Args:
            config: GameConfig object containing generation parameters

        Returns:
            List of randomly generated integers matching the configuration
        """
        pass