import logging

logger = logging.getLogger(__name__)

class Guess:
    """
    A class representing a player's guess in mastermind in each round.
    """
    def __init__(self, numbers: list[int]):
        """
        Initialize a new guess with the provided numbers. (Validated Input)
        
        Args:
            numbers (List[int]): The sequence of numbers for this guess
        """
        self.numbers = numbers
        logger.debug("Created new guess with numbers: %s", self)
    
    def get_numbers(self) -> list[int]:
        """
        Get the numbers in this guess.
        """
        return self.numbers
    
    def __str__(self) -> str:
        """
        Create a string representation of the feedback with desired display format.
        """
        return " ".join(str(num) for num in self.numbers)