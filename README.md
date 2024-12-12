# Mastermind
A Python implementation of the classic code-breaking game with Random.org API integration.

Game Rules
- Computer randomly selects 4 different numbers (0-7)
- Player has 10 attempts to guess the combination
- After each guess, feedback is provided

## Getting Started
### Prerequisites
- Python 3.8+
- pip (Python package installer)

### Installation & Setup

1. Clone the repositor
```
git clone https://github.com/amandayclee/mastermind.git
cd mastermind
```

2. Set up virtual environment
```
python -m venv venv
```

3. Activate virtual environment
```
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

4. Install dependencies
```
pip install -r requirements.txt
```

5. Run the game
```
python main.py
```

6. View the game's test reports
```
pytest
```

7. View the game's documentation using `pydoc`
```
python -m pydoc -b
```

### Thought process
MVP Implementation
1. Basic game mechanics
2. API integration
3. User interface
4. Error handling
5. Testing

### Code Structure


## Next Step
- [ ] Add suppot to give hint
- [ ] Add a configurable "difficulty level" and adjust the numbers that are used
- [ ] Extend to multi-player
- [ ] Keep track of scores
- [ ] Add a timer for the entire game, or each guess attempts
- [x] Develop an event logging system to enhance the development experience
- [x] Enable persistent game storage to allow users to restore their games after exiting the application