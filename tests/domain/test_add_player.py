from pytest import raises

from dice_game.domain.add_player import AddPlayer, AddPlayerRequest
from dice_game.game import DiceGame
from dice_game.player import Player


def test_add_player_adds_a_player(empty_game: DiceGame, add_player: AddPlayer):
    add_player.add_player(empty_game, AddPlayerRequest(player=Player(id=1)))
    assert next(iter(empty_game.players))


def test_add_player_raises_valueerror_player_already_present(
    three_players_game: DiceGame, add_player: AddPlayer
):
    already_present_player = next(iter(three_players_game.players.values()))
    with raises(ValueError, match="Player already in game!"):
        add_player.add_player(
            three_players_game, AddPlayerRequest(player=already_present_player)
        )
