import requests

class Game:
    def __init__(self):
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
    
def test_game_logic():
    game = Game()
    assert game.give_feedback_per_round([4, 5, 6, 7]) == "0 correct number and 0 correction location"
    assert game.give_feedback_per_round([1, 2, 3, 4]) == "3 correct number and 0 correction location"
    assert game.give_feedback_per_round([0, 2, 3, 1]) == "4 correct number and 1 correction location"
    assert game.give_feedback_per_round([2, 1, 5, 3]) == "3 correct number and 2 correction location"

class Player:
    def __init__(self, name):
        self.name = name
        self.all_guess = []
        
    def make_a_guess(self):
        user_guess = Guess(input("Enter your guess: "))
        self.all_guess.append(user_guess)
        user_guess.display_guess()
        
class Guess:
    def __init__(self, guess_string):
        self.guess = [_ for _ in guess_string]
    
    def display_guess(self):
        print("".join(self.guess))
        
player = Player("Mikey")
player.make_a_guess()
        