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

6. Run the test
```
pytest tests/
```

### Thought process
MVP Implementation
1. Basic game mechanics
2. API integration
3. User interface
4. Error handling
5. Testing

### Code Structure
```
MASTERMIND/
├── src/
│   ├── config/
│   │   └── game_config.py     
│   ├── core/
│   │   ├── generators/
│   │   │   ├── base.py        
│   │   │   └── random_org.py  
│   │   └── game.py            
│   ├── interface/
│   │   └── game_interface.py 
│   ├── models/
│   │   ├── feedback.py       
│   │   └── guess.py          
│   └── utils/
│       └── exceptions.py     
├── tests/
│   ├── test_feedback.py
│   ├── test_game.py
│   ├── test_guess.py
│   └── test_number_generator.py
├── main.py                    
└── requirements.txt           
```

## Next Step
- [ ] Add suppot to give hint
- [ ] Add a configurable "difficulty level" and adjust the numbers that are userd
- [ ] Extend to multi-player
- [ ] Keep track of scores
- [ ] Add a timer for the entire game, or each guess attempts
- [ ] Anything else that you can come up with to make the game more fun/interesting that demostrates your backend potential