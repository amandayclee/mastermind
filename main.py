from src.interface.game_interface import GameInterface
from src.core.game import Game

def main():
    game = Game()
    cli = GameInterface()
    cli.set_game(game)
    cli.run_game()

if __name__ == "__main__":
    main()