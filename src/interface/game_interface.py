class GameInterface:
    def __init__(self, game):
        self.game = game
        
    def display_this_game_guess_history(self):
        game_rounds = len(self.game.all_guess_and_feedback)
        print(self.game.code_pattern)
        
        if game_rounds == 0:
            print("It's time for your first guess!")
        else:
            print(f"You've played {game_rounds} rounds!")
            for i in range(game_rounds):
                guess, feedback = self.game.all_guess_and_feedback[i][0], self.game.all_guess_and_feedback[i][1]
                print("Player guesses \"", end = '')
                guess.display()
                print("\", ", end = '')
                feedback.display()
                
    def display_ending_message(self):
        last_feedback_num, last_feedback_num_location = self.game.all_guess_and_feedback[-1][1].correct_number, self.game.all_guess_and_feedback[-1][1].correct_location
        
        if last_feedback_num == len(self.game.code_pattern) and last_feedback_num_location == len(self.game.code_pattern):
            print("Congrats! You win the game!")
        else:
            print("Someone needs more practice maybe.")