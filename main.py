from src.interface.game_interface import GameInterface
from src.core.game import Game
from src.core.generators.random_org import RandomOrgGenerator

def main():
    generator = RandomOrgGenerator()
    game = Game(generator=generator)
    cli = GameInterface()
    cli.set_game(game)
    cli.run_game()

if __name__ == "__main__":
    main()