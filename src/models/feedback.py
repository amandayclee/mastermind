class Feedback:
    def __init__(self, number, location):
        self.correct_number = number
        self.correct_location = location

    def get_feedback(self):
        return [self.correct_number, self.correct_location]