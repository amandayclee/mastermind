from enum import Enum


class GameStatus(Enum):
    """
    Represents the possible states of a Mastermind game.
    - IN_PROGRESS: The game is ongoing and accepting guesses
    - WON: The player has successfully guessed the correct combination
    - LOST: The player has exhausted all attempts without finding the correct combination

    The status transitions work as follows:
    1. Every game starts with IN_PROGRESS
    2. If the player guesses correctly, status changes to WON
    3. If the player uses all attempts without winning, status changes to LOST
    """
    
    IN_PROGRESS = "in_progress"
    WON = "won"
    LOST = "lost"