import pytest
from models.feedback import Feedback


class TestFeedback:
    def test_feedback_intialization(self):
        correct_number, correct_location = 2, 1
        feedback = Feedback(correct_number, correct_location)
        
        assert feedback.correct_number == correct_number
        assert feedback.correct_location == correct_location

    def test_get_feedback(self):
        correct_number, correct_location = 2, 1
        feedback = Feedback(correct_number, correct_location)
        feedback_result = feedback.get_feedback()
        
        assert isinstance(feedback_result, list)
        assert feedback_result == [correct_number, correct_location]
                