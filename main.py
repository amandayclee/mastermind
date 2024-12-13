from src.repository.memory import InMemoryGameRepository
from src.repository.sqlite import SQLiteGameRepository
from src.interface.game_interface import GameInterface
from src.core.game import Game
from src.utils.logging_config import setup_logging_config
from src.services.exceptions.exceptions import GameNotFoundError

def main():
    setup_logging_config()
    cli = GameInterface()
    cli.start_menu()

if __name__ == "__main__":
    main()