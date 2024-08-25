from dataclasses import dataclass
from dice_game.game import DiceGame
from dice_game.player import Player


@dataclass
class AssignCurrentPlayerRequest:
    player: Player


class AssignCurrentPlayer:
    def assign_current_player(
        self, game: DiceGame, request: AssignCurrentPlayerRequest
    ) -> None:
        if request.player not in game.players.values():
            raise ValueError("Player not in game!")

        game.current_player = request.player


