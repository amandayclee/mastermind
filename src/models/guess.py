class Guess:
    def __init__(self, guess_string, timestamp):
        self.guess_array = [_ for _ in guess_string]
        self.timestamp = timestamp
        
    def get_guess(self):
        return self.guess_array