import json
import logging
import sqlite3
from typing import Optional
from src.core.models.game_state import GameState
from src.repository.base import GameRepository
from src.services.exceptions.exceptions import DatabaseError, GameNotFoundError, LoadError, SaveError

logger = logging.getLogger(__name__)

class SQLiteGameRepository(GameRepository):
    """
    SQLite implementation of the game repository for storing and retrieving game states.

    Attributes:
        _db_name (str): Name of the SQLite database file
    """
    def __init__(self, db_name: str = "mastermind.db"):
        """
        Initialize the SQLite repository with specified database name.
        
        Args:
            db_name (str): Name of the database file. Defaults to "mastermind.db"
            
        Raises:
            DatabaseConnectionError: If database initialization fails
        """
        self._db_name = db_name
        logger.info("Initializing SQLite repository with database: %s", db_name)
        self._create_table() 
    
    def _create_table(self):
        """
        Create the games table if it doesn't exist.
        
        Raises:
            DatabaseConnectionError: If table creation fails
        """
        connection = None
        
        try:
            logger.debug("Attempting to create games table")
            connection = sqlite3.connect(self._db_name)
            connection.execute("""
                CREATE TABLE IF NOT EXISTS games (
                    game_id TEXT PRIMARY KEY,
                    code_pattern TEXT NOT NULL,
                    status TEXT NOT NULL,
                    attempts INTEGER NOT NULL,
                    guess_records TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL,
                    config TEXT NOT NULL
                )
            """)
            connection.commit()
            logger.info("Games table created successfully")
            
        except sqlite3.Error as e:
            logger.error("Failed to create table: %s", str(e))
            raise DatabaseError(f"Cannot create initial table: {str(e)}")

        finally:
            if connection:
                    connection.close()

    def save_game(self, game_state: GameState) -> None:
        """
        Save or update a game state in the database.
    
        Args:
            game_state (GameState): The game state to save
            
        Raises:
            SaveError: If saving the game state fails
            
        """
        connection = None
        
        try: 
            logger.debug("Saving game state - ID: %s, Status: %s, Attempts: %d",
                        game_state.game_id, game_state.status, game_state.attempts)
            connection = sqlite3.connect(self._db_name)
            data = game_state.to_db_format()
            
            try:
                connection.execute("""
                    INSERT OR REPLACE INTO games (
                        game_id, code_pattern, status, attempts,
                        guess_records, created_at, updated_at, config
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    data["game_id"],
                    json.dumps(data["code_pattern"]),
                    data["status"],
                    data["attempts"],
                    json.dumps(data["guess_records"]),
                    data["created_at"],
                    data["updated_at"],
                    json.dumps(data["config"])
                ))
            except TypeError as e:
                logger.error("Failed to save the state %s: %s", game_state.game_id, str(e))
                raise SaveError(f"Invalid game state data: {str(e)}")
            
            connection.commit()
            logger.debug("Game state saved successfully")
            
        except sqlite3.Error as e:
            logger.error("Failed to save game %s: %s", game_state.game_id, str(e))
            if connection:
                connection.rollback()
            raise SaveError(f"Cannot save the game: {str(e)}")

        finally:
            if connection:
                    connection.close()
                
    def load_game(self, game_id: str) -> GameState:
        """
        Load a game state from the database by its ID.
        
        Args:
            game_id (str): The unique identifier of the game to load
            
        Returns:
            GameState: The loaded game state
            
        Raises:
            GameNotFoundError: If no game exists with the given ID
            LoadError: If loading or decoding the game data fails

        """
        connection = None
        
        try:
            connection = sqlite3.connect(self._db_name)
            cursor = connection.execute("""
                SELECT code_pattern, status, attempts,
                       guess_records, created_at, updated_at, config
                FROM games WHERE game_id = ?
            """, (game_id,))
            
            game_data = cursor.fetchone()
            
            if game_data is None:
                logger.warning("Game not found - ID: %s", game_id)
                raise GameNotFoundError(game_id)

            data = {
                "game_id": game_id,
                "code_pattern": json.loads(game_data[0]),
                "status": game_data[1],
                "attempts": game_data[2],
                "guess_records": json.loads(game_data[3]),
                "created_at": game_data[4],
                "updated_at": game_data[5],
                "config": json.loads(game_data[6])
            }
            
            logger.debug("Game state loaded successfully")
            return GameState.from_db_format(data)
        
        except sqlite3.Error as e:
            logger.error("Failed to load game %s: %s", game_id, str(e))
            raise LoadError()
        
        finally:
            if connection:
                connection.close()
