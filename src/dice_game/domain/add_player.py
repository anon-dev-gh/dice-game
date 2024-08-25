from dataclasses import dataclass

from dice_game.game import DiceGame
from dice_game.player import Player


@dataclass
class AddPlayerRequest:
    player: Player


class AddPlayer:
    def add_player(self, game: DiceGame, request: AddPlayerRequest) -> None:
        player = request.player
        if player.id in game.players:
            raise ValueError("Player already in game!")
        game.players[player.id] = player
