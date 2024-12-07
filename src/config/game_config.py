class GameConfig():
    def __init__(self, pattern_length=4, min_number=0, max_number=7, max_attempts=10):
        self.pattern_length = pattern_length
        self.min_number = min_number
        self.max_number = max_number
        self.max_attempts = max_attempts
        
        self.api_base_url = "https://www.random.org/integers/"
        
    def get_api_params(self):
        return {
            "num": str(self.pattern_length),
            "min": str(self.min_number),
            "max": str(self.max_number),
            "col": str(self.pattern_length),
            "base": "10",
            "format": "plain",
            "rnd": "new",
        }
