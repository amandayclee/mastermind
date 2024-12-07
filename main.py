from src.interface.game_interface import GameInterface
from src.models.player import Player


print("Welcome to the mastermind game!")

name = input("What's your name? ")
player = Player(name)

print("Great, now let's start the game.")

game = player.start_new_game()
game_interface = GameInterface(game)


while game.can_keep_play:
    game_interface.display_this_game_guess_history()
    
    guess_string = input("What's your guess? ")
    game.give_feedback_per_round(guess_string)

game_interface.display_ending_message()