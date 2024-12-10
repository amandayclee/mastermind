class GameConfig():
    def __init__(self, 
                 pattern_length: int = 4, 
                 min_number: int = 0, 
                 max_number: int = 7, 
                 max_attempts: int = 10) -> None:
        self.pattern_length = pattern_length
        self.min_number = min_number
        self.max_number = max_number
        self.max_attempts = max_attempts