# src/dice_game/game.py

from typing import Dict, Optional

from dice_game.player import Player


class DiceGame:
    def __init__(self) -> None:
        self.players: Dict[int, Player] = {}
        self.scores: Dict[int, int] = {}
        self.current_player: Optional[Player] = None

    def finish_turn(self, player_id: int):
        return self.scores[player_id]

    def check_game_over(self) -> bool:
        return any(score >= 50 for score in self.scores.values())

    def end_game(self):
        winner_id = max(self.scores, key=self.scores.get)
        return winner_id, self.scores[winner_id]
