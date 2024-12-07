# Mastermind
Game Rules

Computer vs. Player
code_maker = computer
code_breaker = player

code maker makes a pattern of 4 different number from total 8 different numbers
-> use Random Number Generator API

code breaker can guess from [0, 1, 2, 3, 4, 5, 6, 7]
format "2 2 4 6" all string with white space, and the game match it with the code maker's pattern
-> all correct
-> # of correct number and # of correct location

code breaker has 10 attemps



## Getting Started
### How to run the code

1. Clone the repositor
```
git clone https://github.com/amandayclee/mastermind.git
cd mastermind
```

2. Install Hatch if you haven't
```
pip install hatch
```

3. Create environment and run
```
hatch env create
hatch run python src/main.py
```

### Thought process
1. Think about the userflow
- When the application starts, ask the user to play a game
- After the "game" startes, generate a code_pattern, and "user" can make a guess
- For each "guess", game will give a "feedback" according to the game rule
- The "interface" of certain game will display the player's guess and feedback, and the turns remaining

2. List all of class we might need
- Game:
    - State:
        - code pattern (Duplicate numbers are allowed)
        - (score)
        - all guess and feedback

    - Method:
        - make a guess
        - check guess and give feedback
        - calculate scores

- Game Interface
    - Method:
        - get_game to display player'guess and feedback
        - view the history of guesses and their feedback
        - view the number of guesses remaining is displayed

- Player: contains the attemps player make
    - State:
        - game_history

    Method:
        - start a game

- Guess: each guess player makes
    State:
        - guess array
        - time stamp
    
    Method:
    - display guess


- Feedback
    State:
        - correct number
        - correct location

    Method:
    - display feedback

3. Code the basic classes

### Code Structure

## Next Step
- [ ] Add suppot to give hint
- [ ] Add a configurable "difficulty level" and adjust the numbers that are userd
- [ ] Extend to multi-player
- [ ] Keep track of scores
- [ ] Add a timer for the entire game, or each guess attempts
- [ ] Anything else that you can come up with to make the game more fun/interesting that demostrates your backend potential