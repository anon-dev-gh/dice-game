from dice_game.game import DiceGame
from dice_game.player import Player


def test_player_roll():
    player = Player(player_id=1, name="Alice")
    roll = player.roll_dice()
    assert 2 <= roll <= 12


def test_game_turn():
    players = [Player(player_id=1, name="Alice"), Player(player_id=2, name="Bob")]
    game = DiceGame(players)
    game.play_turn()
    assert players[0].turns_taken == 1
    assert players[1].turns_taken == 1
