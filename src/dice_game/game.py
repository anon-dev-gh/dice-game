from typing import MutableMapping

from dice_game.dispatcher import EventDispatcher
from dice_game.events import (
    GameOverEvent,
    PlayerJoinsEvent,
    PlayerRollsEvent,
    TurnFinishedEvent,
)


class DiceGame:
    def __init__(self, dispatcher: EventDispatcher):
        self.dispatcher = dispatcher
        self.player_names_by_ids: MutableMapping[int, str] = {}

    def add_player(self, player_id: int, player_name: str):
        self.player_names_by_ids[player_id] = player_name
        event = PlayerJoinsEvent(player_id=player_id, player_name=player_name)
        self.dispatcher.dispatch(event)

    def roll_dice(self, player_id: int):
        import random

        roll_result = random.randint(1, 6)
        event = PlayerRollsEvent(player_id=player_id, roll_result=roll_result)
        self.dispatcher.dispatch(event)
        return roll_result

    def finish_turn(self, player_id: int, score: int):
        event = TurnFinishedEvent(player_id=player_id, score=score)
        self.dispatcher.dispatch(event)

    def end_game(self):
        winner_id = max(
            self.player_names_by_ids.keys(), key=lambda pid: self.players[pid]
        )
        winner_score = sum(self.roll_dice(winner_id) for _ in range(3))
        event = GameOverEvent(winner_id=winner_id, winner_score=winner_score)
        self.dispatcher.dispatch(event)
