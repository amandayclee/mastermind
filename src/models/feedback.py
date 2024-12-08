class Feedback:
    def __init__(self, numbers_correct: int, positions_correct: int):
        """
        initialize a feedback for a guess
        """
        self.numbers_correct = numbers_correct
        self.positions_correct = positions_correct
    
    def is_winning_guess(self, code_length: int) -> bool:
        """
        check if the guess is right for both numbers and positions
        """
        return self.positions_correct == code_length
    
    def __str__(self) -> str:
        """for display"""
        return f"{self.numbers_correct} correct numbers and {self.positions_correct} correct positions"