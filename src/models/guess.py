from datetime import datetime

class Guess:
    def __init__(self, numbers: list[int]):
        """
        initialize a validated guess
        """
        self.numbers = numbers
        self.timestamp = datetime.now()
    
    def get_numbers(self) -> list[int]:
        """get guess number"""
        return self.numbers
    
    def __str__(self) -> str:
        """for display"""
        return " ".join(str(num) for num in self.numbers)