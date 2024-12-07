def test_game_logic():
    game = Game()
    assert game.give_feedback_per_round([4, 5, 6, 7]) == "0 correct number and 0 correction location"
    assert game.give_feedback_per_round([1, 2, 3, 4]) == "3 correct number and 0 correction location"
    assert game.give_feedback_per_round([0, 2, 3, 1]) == "4 correct number and 1 correction location"
    assert game.give_feedback_per_round([2, 1, 5, 3]) == "3 correct number and 2 correction location"
