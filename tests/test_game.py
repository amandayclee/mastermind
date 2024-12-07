from datetime import datetime
from unittest.mock import Mock, patch
import pytest
from models.feedback import Feedback
from models.game import Game
from models.guess import Guess


class TestGame:
    @pytest.fixture
    def mock_api(self):
        mock = Mock()
        mock.text = "1\t2\t3\t4"
        mock.raise_for_status = Mock()
        
        return mock
    
    def test_game_initialization(self, mock_api):
        with patch('requests.get', return_value=mock_api):
            game = Game()
            
            assert game.can_keep_play == True
            assert game.guess_time == 0
            assert len(game.all_guess_and_feedback) == 0
            assert game.code_pattern == [1, 2, 3, 4]
    
    def test_check_number(self, mock_api):
        with patch('requests.get', return_value=mock_api):
            game = Game()
            game.code_pattern = [1, 2, 3, 4]
            game.pattern_count = {1: 1, 2: 1, 3: 1, 4: 1}
            
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            
            guess1 = Guess([1, 2, 3, 4], timestamp)
            guess2 = Guess([5, 6, 7, 8], timestamp)
            guess3 = Guess([1, 5, 6, 7], timestamp)
            
            assert game.check_number(guess1) == 4
            assert game.check_number(guess2) == 0
            assert game.check_number(guess3) == 1
            
    def test_check_location(self, mock_api):
        with patch('requests.get', return_value=mock_api):
            game = Game()
            game.code_pattern = [1, 2, 3, 4]
            game.pattern_count = {1: 1, 2: 1, 3: 1, 4: 1}
            
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            
            guess1 = Guess([1, 2, 3, 4], timestamp)
            guess2 = Guess([5, 6, 7, 8], timestamp)
            guess3 = Guess([1, 2, 6, 7], timestamp)

            assert game.check_location(guess1) == 4
            assert game.check_location(guess2) == 0
            assert game.check_location(guess3) == 2            
    
    def test_give_feedback_per_round(self, mock_api):
        
        with patch('requests.get', return_value=mock_api):
            game = Game()
            game.code_pattern = [1, 2, 3, 4]
            game.pattern_count = {1: 1, 2: 1, 3: 1, 4: 1}
            
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            guess = Guess([1, 2, 3, 4], timestamp)
            
            game.give_feedback_per_round(guess)
            
            assert len(game.all_guess_and_feedback) == 1
            assert game.guess_time == 1
            assert isinstance(game.all_guess_and_feedback[0][0], Guess)
            assert isinstance(game.all_guess_and_feedback[0][1], Feedback)
          
            
    def test_game_end_conditions(self, mock_api):
        
        with patch('requests.get', return_value=mock_api):
            game = Game()
            game.code_pattern = [1, 2, 3, 4]
            game.pattern_count = {1: 1, 2: 1, 3: 1, 4: 1}
            timestamp = ddatetime.now().strftime('%Y-%m-%d %H:%M:%S')
            
            guess_correct = Guess([1, 2, 3, 4], timestamp)
            game.give_feedback_per_round(guess_correct)
            assert game.can_keep_play == False
            
            game = Game() 
            guess_wrong = Guess([5, 6, 7, 8], timestamp)
            for _ in range(10):
                game.give_feedback_per_round(guess_wrong)
            assert game.can_keep_play == False