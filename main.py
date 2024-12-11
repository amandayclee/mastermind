from src.core.repository.memory import InMemoryGameRepository
from src.interface.game_interface import GameInterface
from src.core.game import Game
from src.utils.logging_config import setup_logging_config
from src.utils.exceptions import GameNotFoundError

def main():
    setup_logging_config()
    repository = InMemoryGameRepository()
    
    while True:
        print("\n****** Mastermind ******")
        print("1. New Game")
        print("2. Load Game (Current Session Only)")
        print("3. Exit Program")
        choice = input("Select an option (1-3): ")
        
        if choice == "1":
            game = Game(repository=repository)
            cli = GameInterface()
            cli.set_game(game)
            cli.run_game()
        elif choice == "2":
            game_id = input("Enter your game ID: ")
            try:
                game = Game(repository=repository, game_id=game_id)
                cli = GameInterface()
                cli.set_game(game)
                cli.run_game()
            except GameNotFoundError:
                print(f"No game found with ID: {game_id}")
        elif choice == "3":
            print("Thanks for playing!")
            break
        else:
            print("Invalid choice. Please select 1, 2, or 3")

if __name__ == "__main__":
    main()