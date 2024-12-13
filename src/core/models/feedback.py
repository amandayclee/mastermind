import logging

logger = logging.getLogger(__name__)

class Feedback:
    """
    A class to represent feedback for a guess in mastermind in each round.
    """
    def __init__(self, numbers_correct: int, positions_correct: int):
        """
        Initialize a new Feedback instance.
        
        Attributes:
            numbers_correct (int): Number of correct digits regardless of position
            positions_correct (int): Number of digits that are both correct and in the correct position
        """
        self.numbers_correct = numbers_correct
        self.positions_correct = positions_correct
        
        logger.debug("Created feedback - Numbers correct: %d, Positions correct: %d",
                    numbers_correct, positions_correct)
        
    def is_winning_guess(self, code_length: int) -> bool:
        """
        Determine if the current feedback represents a winning guess, where it get the number of correct locations equals to the length of  the code pattern.
        
        Args:
            code_length (int): The length of the code pattern
            
        Returns:
            bool: True if this feedback represents a winning guess, False otherwise
        """
        return self.positions_correct == code_length
    
    def __str__(self) -> str:
        """
        Create a string representation of the feedback with desired display format.
        
        Returns:
            str: A formatted string describing the feedback
        """
        return f"{self.numbers_correct} correct numbers and {self.positions_correct} correct positions"