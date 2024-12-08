class GameConfig():
    def __init__(self, pattern_length=4, min_number=0, max_number=7, max_attempts=10):
        self.pattern_length = pattern_length
        self.min_number = min_number
        self.max_number = max_number
        self.max_attempts = max_attempts