from src.interface.game_interface import GameInterface
from src.core.game import Game
from src.utils.logging_config import setup_logging_config

def main():
    setup_logging_config()
    game = Game()
    cli = GameInterface()
    cli.set_game(game)
    cli.run_game()

if __name__ == "__main__":
    main()