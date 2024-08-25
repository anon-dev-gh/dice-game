from dataclasses import dataclass
from random import randint

from dice_game.game import DiceGame
from dice_game.player import Player


@dataclass
class RollDiceRequest:
    player: Player


class RollDice:
    def roll_dice(self, game: DiceGame, request: RollDiceRequest) -> int:
        if request.player not in game.players.values():
            raise ValueError("Player not in game!")
        
        if game.current_player != request.player:
            raise ValueError("It's not this player's turn!")
        
        return randint(1, 6)