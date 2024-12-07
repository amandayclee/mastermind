class Player:
    def __init__(self, name):
        self.name = name
        self.all_guess = []
        self.all_feedback = []
        
    def make_a_guess(self, user_guess):
        self.all_guess.append(user_guess)
        
    def receive_a_feedback(self, guess_feedback):
        self.all_feedback.append(guess_feedback)