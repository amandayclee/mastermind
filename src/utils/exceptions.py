class GuessError(Exception):
    """basic guess error"""
    def __init__(self, message="An error occurred"):
        self.message = message
        super().__init__(self.message) 
        
class InvalidLengthError(GuessError):
    """length not match error"""
    def __init__(self, expected_length, actual_length):
        message = f"Guess must be {expected_length} digits long, got {actual_length}"
        super().__init__(message)
        
class RangeError(GuessError):
    """number range not match error"""
    def __init__(self):
        message = "Numbers must be between 0 and 7"
        super().__init__(message)

class GeneratorError(Exception):
    """code pattern generation not success"""
    def __init__(self, message="Generator error occurred"):
        self.message = message
        super().__init__(self.message)

class GameInitError(Exception):
    """game initialization not success"""
    def __init__(self, message="Failed to initialize game"):
        self.message = message
        super().__init__(self.message)