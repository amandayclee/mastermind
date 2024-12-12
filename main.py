from src.core.repository.memory import InMemoryGameRepository
from src.core.repository.sqlite import SQLiteGameRepository
from src.interface.game_interface import GameInterface
from src.core.game.game import Game
from src.utils.logging_config import setup_logging_config
from src.utils.exceptions import GameNotFoundError

def main():
    setup_logging_config()
    cli = GameInterface()
    cli.start_menu()

if __name__ == "__main__":
    main()