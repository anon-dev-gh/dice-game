from pytest import fixture

from dice_game.dependencies import solve
from dice_game.domain.add_player import AddPlayer, AddPlayerRequest
from dice_game.domain.assign_current_player import (
    AssignCurrentPlayer,
    AssignCurrentPlayerRequest,
)
from dice_game.game import DiceGame
from dice_game.player import Player


@fixture
def empty_game():
    return solve(DiceGame)


@fixture
def add_player():
    return solve(AddPlayer)


@fixture
def assign_current_player():
    return solve(AssignCurrentPlayer)


@fixture
def three_players_game(
    add_player: AddPlayer,
    assign_current_player: AssignCurrentPlayer,
) -> DiceGame:
    # Rather than reusing empty_game fixture that could lead to nasty bugs, we instantiate it here.
    game = DiceGame()
    add_player.add_player(game, AddPlayerRequest(player=Player(id=1)))
    add_player.add_player(game, AddPlayerRequest(player=Player(id=2)))
    add_player.add_player(game, AddPlayerRequest(player=Player(id=3)))

    assign_current_player.assign_current_player(
        game, AssignCurrentPlayerRequest(player=game.players[1])
    )

    return game
