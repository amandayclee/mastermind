class Feedback:
    def __init__(self, number, location):
        self.correct_number = number
        self.correct_location = location
        
    def display(self):
        print(f"{self.correct_number} correct number and {self.correct_location} correction location")