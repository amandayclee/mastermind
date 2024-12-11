from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict, List, Tuple

from src.config.game_config import GameConfig
from src.models.feedback import Feedback
from src.models.guess import Guess
from src.models.game_status import GameStatus


@dataclass
class GameState:
    game_id: str
    code_pattern: List[int]
    status: GameStatus
    attempts: int
    guess_records: List[Tuple[Guess, Feedback]]
    created_at: datetime
    updated_at: datetime
    config: GameConfig
    
    def to_db_format(self) -> Dict[str, Any]:
        temp_guess_records = []
        for guess, feedback in self.guess_records:
            temp_dict = {
                "guess": guess.get_numbers(),
                "feedback": {
                    "numbers_correct": feedback.numbers_correct,
                    "positions_correct": feedback.positions_correct
                }
            }
            temp_guess_records.append(temp_dict)
        
        return {
                "game_id": self.game_id,
                "code_pattern": self.code_pattern,
                "status": self.status.value,
                "attempts": self.attempts,
                "guess_records": temp_guess_records,
                "created_at": self.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                "updated_at": self.updated_at.strftime("%Y-%m-%d %H:%M:%S"),
                "config": {
                    "pattern_length": self.config.pattern_length,
                    "max_attempts": self.config.max_attempts,
                    "min_number": self.config.min_number,
                    "max_number": self.config.max_number
                }
        }
    
    @classmethod
    def from_db_format(cls, data: Dict[str, Any]) -> 'GameState':
        temp_guess_records = []
        for record in data["guess_records"]:
            temp_tuple = (
                Guess(record["guess"]),
                Feedback(record["feedback"]["numbers_correct"], record["feedback"]["positions_correct"])
            )
            temp_guess_records.append(temp_tuple)
            
        config = GameConfig(
            pattern_length=data["config"]["pattern_length"],
            max_attempts=data["config"]["max_attempts"],
            min_number=data["config"]["min_number"],
            max_number=data["config"]["max_number"]
        )
        
        return cls(
            game_id = data["game_id"],
            code_pattern = data["code_pattern"],
            status = GameStatus(data["status"]),
            attempts = data["attempts"],
            guess_records = temp_guess_records,
            created_at = datetime.strptime(data["created_at"], "%Y-%m-%d %H:%M:%S"),
            updated_at = datetime.strptime(data["updated_at"], "%Y-%m-%d %H:%M:%S"),
            config=config
        )