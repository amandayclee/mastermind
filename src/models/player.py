from src.models.game import Game


class Player:
    def __init__(self, name):
        self.name = name
        self.game_history = []
        
    def start_new_game(self):
        game = Game()
        self.game_history.append(game)
        
        return game