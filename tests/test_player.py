import pytest
from models.game import Game
from models.player import Player


class TestPlayer:
    def test_player_initialization(self):
        player_name = "Mike"
        player = Player(player_name)
        
        assert player.name == player_name
        assert player.game_history == []
        
    def test_first_game(self):
        player = Player("Mike")
        game = player.start_new_game()
        
        assert isinstance(game, Game)
        assert len(player.game_history) == 1
        assert player.game_history[0] == game
        
    def test_multiple_games(self):
        player = Player("Mike")
        
        game1 = player.start_new_game()
        game2 = player.start_new_game()
        
        assert len(player.game_history) == 2
        assert player.game_history[0] == game1
        assert player.game_history[1] == game2
        assert game1 != game2