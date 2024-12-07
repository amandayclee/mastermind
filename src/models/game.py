import requests
from src.models.guess import Guess
from src.models.feedback import Feedback
from datetime import datetime

class Game:
    def __init__(self):
        self.can_keep_play = True
        self.pattern_count = {}
        self.code_pattern = self._generate_code_pattern()
        self.guess_time = 0
        self.all_guess_and_feedback = []
        
    def _generate_code_pattern(self):
        num = '4'
        min = '0'
        max = '7'
        base = '10'
        format = 'plain'
        col = '4'
        rnd = 'new'
        api_link = f"https://www.random.org/integers/?num={num}&min={min}&max={max}&col={col}&base={base}&format={format}&rnd={rnd}"
        
        # TODO handle response error
        response = requests.get(api_link)
        code_pattern = response.text.strip("\n").split("\t")
        
        for num in code_pattern:
            self.pattern_count[num] = self.pattern_count.get(num, 0) + 1
        
        print(self.pattern_count)
        
        return code_pattern
              
    # TODO change guess_string from a string to a Guess object so that you can do error
    # handling inside of the interface.
    def give_feedback_per_round(self, guess):
        correct_number = self.check_number(guess)
        correct_location = self.check_location(guess)
        feedback = Feedback(correct_number, correct_location)
        self.all_guess_and_feedback.append((guess, feedback))
        self.guess_time += 1
        self.can_keep_play = self.check_game(correct_number, correct_location)
        
    def check_game(self, correct_number, correct_location):
        if (correct_number == len(self.code_pattern) and correct_location == len(self.code_pattern)) or \
            self.guess_time == 10:
            return False
        else:
            return True
        
    def check_number(self, player_guess):
        player_guess = player_guess.get_guess()
        correct_number = 0
        pattern_count_copy = self.pattern_count.copy()
        
        for i in range(len(player_guess)):
            if player_guess[i] in self.code_pattern and pattern_count_copy[player_guess[i]] != 0:
                correct_number += 1
                pattern_count_copy[player_guess[i]] -= 1
        
        return correct_number
    
    def check_location(self, player_guess):
        player_guess = player_guess.get_guess()
        correct_location = 0
        
        for i in range(len(player_guess)):
            if player_guess[i] == self.code_pattern[i]:
                correct_location += 1
        
        return correct_location