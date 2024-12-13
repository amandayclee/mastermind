from dataclasses import dataclass
from datetime import datetime
import logging
from typing import Any, Dict, List, Tuple

from src.core.config.game_config import GameConfig
from src.core.models.feedback import Feedback
from src.core.models.game_difficulty import Difficulty
from src.core.models.guess import Guess
from src.core.models.game_status import GameStatus

logger = logging.getLogger(__name__)

@dataclass
class GameState:
    """
    A complete state for a masterming game session, can be saved and restored for repository use.
    
    The state includs:
    - Unique identifier for the game
    - Code pattern for player to crack
    - Current game status
    - Number of attempt made by the player
    - Complete guess history and each guess' feedback
    - Timestamp the game initialized
    - Timestamp the state updated
    - Game configuration setting
    
    Attributes:
        game_id (str): Unique identifier for the game session
        code_pattern (List[int]): The secret code players try to guess
        status (GameStatus): Current state of the game
        attempts (int): Number of guesses made so far
        guess_records (List[Tuple[Guess, Feedback]]): History of all guesses and their feedback
        created_at (datetime): When the game was started
        updated_at (datetime): When the game was last modified
        config (GameConfig): Configuration settings for this game
    """
    
    game_id: str
    code_pattern: List[int]
    status: GameStatus
    attempts: int
    guess_records: List[Tuple[Guess, Feedback]]
    created_at: datetime
    updated_at: datetime
    config: GameConfig
    
    def to_db_format(self) -> Dict[str, Any]:
        """
        Convert the game state to a format suitable for database storage.
        Complex data format like each record in guess_records is converted from Tuple to dict.
        Guess object inside each record is converted to simple list.
        Feedback object each record is converted to simple dict.

        Returns:
            Dict[str, Any]: Database-friendly representation of the game state
        """
        logger.debug("Converting game state to database format - ID: %s, Status: %s, Attempts: %d",
                    self.game_id, self.status, self.attempts)
        
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
        
        logger.debug("Successfully converted game state to database format - Records count: %d",
                    len(temp_guess_records))
        
        return {
                "game_id": self.game_id,
                "code_pattern": self.code_pattern,
                "status": self.status.value,
                "attempts": self.attempts,
                "guess_records": temp_guess_records,
                "created_at": self.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                "updated_at": self.updated_at.strftime("%Y-%m-%d %H:%M:%S"),
                "config": {
                "difficulty": self.config.difficulty.value
            }
        }
    
    @classmethod
    def from_db_format(cls, data: Dict[str, Any]) -> 'GameState':
        """
        Create a GameState instance from database-formatted data.
        This class method reconstructs a GameState object from its serialized
        database representation.

        Args:
            data (Dict[str, Any]): The database representation of a game state

        Returns:
            GameState: A new GameState instance representing the stored game
        """
        logger.debug("Reconstructing game state - ID: %s, Status: %s, Records: %d",
                    data.get('game_id'), data.get('status'), len(data.get('guess_records', [])))
        temp_guess_records = []
        
        for record in data["guess_records"]:
            temp_tuple = (
                Guess(record["guess"]),
                Feedback(record["feedback"]["numbers_correct"], record["feedback"]["positions_correct"])
            )
            temp_guess_records.append(temp_tuple)
            
        difficulty = Difficulty(data["config"].get("difficulty", Difficulty.NORMAL.value))
        config = GameConfig(difficulty=difficulty)
        
        logger.debug("Successfully reconstructed game state for ID: %s", data.get('game_id'))
        
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