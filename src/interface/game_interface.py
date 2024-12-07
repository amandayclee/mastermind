from datetime import datetime
from src.models.guess import Guess
from src.models.player import Player


class GameInterface:
    def __init__(self):
        self.game = None
        
    def set_game(self, game):
        self.game = game
        
    def create_player(self):
        print("Welcome to the mastermind game!")
        name = input("What's your name? ")
        player = Player(name)
        print(f"Great {name}, now let's start the game.")
        
        return player
    
    def run_game(self):
        while self.game.can_keep_play:
            self.display_game_guess_history()
            guess = Guess(input("What's your guess? "), datetime.today().strftime('%Y-%m-%d %H:%M:%S'))
            # TODO validate the guess. 
            # Make sure the length is correct
            # Make sure they are all valid numbers from 0-7
            self.game.give_feedback_per_round(guess)
            
        self.display_ending_message()
            
    def display_game_guess_history(self):
        game_rounds = len(self.game.all_guess_and_feedback)
        print(self.game.code_pattern)
        
        if game_rounds == 0:
            print("It's time for your first guess!")
        else:
            print(f"You've played {game_rounds} rounds!")
            for i in range(game_rounds):
                guess, feedback = self.game.all_guess_and_feedback[i][0], self.game.all_guess_and_feedback[i][1]
                guess_display =  " ".join(guess.get_guess())
                feedback_display =  f"{feedback.get_feedback()[0]} correct number and {feedback.get_feedback()[1]} correction location"
                
                print("Player guesses \"" + guess_display + "\", " + feedback_display)
                
    def display_ending_message(self):
        last_feedback_num, last_feedback_num_location = self.game.all_guess_and_feedback[-1][1].correct_number, self.game.all_guess_and_feedback[-1][1].correct_location
        
        if last_feedback_num == len(self.game.code_pattern) and last_feedback_num_location == len(self.game.code_pattern):
            print("Congrats! You win the game!")
        else:
            print("Someone needs more practice maybe.")