from src.interface.game_interface import GameInterface

game_interface = GameInterface()
player = game_interface.create_player()
game = player.start_new_game()
game_interface.set_game(game)
game_interface.run_game()
