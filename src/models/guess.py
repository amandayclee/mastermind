class Guess:
    def __init__(self, guess_string, timestamp):
        self.guess_array = [_ for _ in guess_string]
        self.timestamp = timestamp
        
    def display(self):
        temp = []
        for num in self.guess_array:
            temp.append(num)
        print(" ".join(temp), end = '')