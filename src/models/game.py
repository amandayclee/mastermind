import requests
from src.models import Feedback

class Game:
    def __init__(self, player):
        self.player = player
        self.code_pattern = Game.__generate_code_pattern()
       
    @staticmethod 
    def __generate_code_pattern():
        num = '4'
        min = '0'
        max = '7'
        base = '10'
        format = 'plain'
        col = '4'
        rnd = 'new'
        api_link = f"https://www.random.org/integers/?num={num}&min={min}&max={max}&col={col}&base={base}&format={format}&rnd={rnd}"
        
        response = requests.get(api_link)
        code_pattern = response.text.strip("\n").split("\t")
        
        return code_pattern
        
    def give_feedback_per_round(self, player_guess):
        correct_number = self.check_number(player_guess)
        correct_location = self.check_location(player_guess)
        feedback = Feedback(correct_number, correct_location)
        self.player.receive_a_feedback(feedback)
        
        return (f"{correct_number} correct number and {correct_location} correction location")
        
    def check_number(self, player_guess):
        correct_number = 0
        
        for i in range(len(player_guess)):
            if player_guess[i] in self.code_pattern:
                correct_number += 1
        
        return correct_number
    
    def check_location(self, player_guess):
        correct_location = 0
        
        for i in range(len(player_guess)):
            if player_guess[i] == self.code_pattern[i]:
                correct_location += 1
        
        return correct_location