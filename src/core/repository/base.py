from abc import ABC, abstractmethod

from src.models.game_status import GameStatus


class GameRepository(ABC):
    @abstractmethod
    def save_game(self, game_state: GameStatus):
        pass
    
    @abstractmethod
    def load_game(self, game_id: str):
        pass
    
    