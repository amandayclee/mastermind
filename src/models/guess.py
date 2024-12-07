class Guess:
    def __init__(self, guess_string, timestamp):
        self.guess = [_ for _ in guess_string]
        self.timestamp = timestamp