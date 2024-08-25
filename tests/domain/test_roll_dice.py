from pytest import fixture, raises

from dice_game.domain.roll_dice import RollDice, RollDiceRequest
from dice_game.game import DiceGame
from dice_game.player import Player


@fixture
def roll_dice():
    return RollDice()


def test_roll_dice_returns_valid_number(
    three_players_game: DiceGame, roll_dice: RollDice
):
    current_player = three_players_game.current_player
    assert current_player, "expected current_player"
    result = roll_dice.roll_dice(
        three_players_game, RollDiceRequest(player=current_player)
    )
    assert 1 <= result <= 6


def test_roll_dice_raises_valueerror_player_not_in_game(
    three_players_game: DiceGame, roll_dice: RollDice
):
    non_existent_player = Player(id=999)
    with raises(ValueError, match="Player not in game!"):
        roll_dice.roll_dice(
            three_players_game, RollDiceRequest(player=non_existent_player)
        )


def test_roll_dice_raises_valueerror_not_players_turn(
    three_players_game: DiceGame, roll_dice: RollDice
):
    not_current_player = next(
        player
        for player in three_players_game.players.values()
        if player != three_players_game.current_player
    )
    with raises(ValueError, match="It's not this player's turn!"):
        roll_dice.roll_dice(
            three_players_game, RollDiceRequest(player=not_current_player)
        )
