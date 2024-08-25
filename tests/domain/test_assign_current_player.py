import pytest

from dice_game.domain.assign_current_player import AssignCurrentPlayerRequest
from dice_game.player import Player


def test_assign_current_player(three_players_game, assign_current_player):
    player = three_players_game.players[1]
    request = AssignCurrentPlayerRequest(player=player)

    assign_current_player.assign_current_player(three_players_game, request)

    assert three_players_game.current_player == player


def test_assign_current_player_not_in_game(three_players_game, assign_current_player):
    player_not_in_game = Player(4)
    request = AssignCurrentPlayerRequest(player=player_not_in_game)

    with pytest.raises(ValueError, match="Player not in game!"):
        assign_current_player.assign_current_player(three_players_game, request)


def test_assign_current_player_changes_current_player(
    three_players_game, assign_current_player
):
    initial_player = three_players_game.players[1]
    new_player = three_players_game.players[2]
    three_players_game.current_player = initial_player

    request = AssignCurrentPlayerRequest(player=new_player)
    assign_current_player.assign_current_player(three_players_game, request)

    assert three_players_game.current_player == new_player
    assert three_players_game.current_player != initial_player
