# src/dice_game/message_parser.py

import json
from typing import Callable, Dict, Optional

from dice_game.events import (
    Event,
    GameOverEvent,
    PlayerJoinsEvent,
    PlayerRollsEvent,
    TurnFinishedEvent,
)


class MessageParser:
    def __init__(self) -> None:
        self.handlers: Dict[str, Callable[[Dict], Event]] = {
            "join": self.handle_join,
            "roll": self.handle_roll,
            "finish_turn": self.handle_finish_turn,
            "end_game": self.handle_end_game,
        }

    def parse_message(self, message: str) -> Optional[Event]:
        data = json.loads(message)
        event_type = data.get("event")

        if handler := self.handlers.get(event_type):
            return handler(data)
        else:
            print(f"Unknown event type: {event_type}")
            return None

    def handle_join(self, data: Dict) -> Event:
        return PlayerJoinsEvent(
            player_id=data["player_id"], player_name=data["player_name"]
        )

    def handle_roll(self, data: Dict) -> Event:
        return PlayerRollsEvent(
            player_id=data["player_id"], roll_result=data.get("roll_result", 0)
        )

    def handle_finish_turn(self, data: Dict) -> Event:
        return TurnFinishedEvent(
            player_id=data["player_id"], score=data.get("score", 0)
        )

    def handle_end_game(self, data: Dict) -> Event:
        return GameOverEvent(
            winner_id=data["player_id"], winner_score=data.get("winner_score", 0)
        )
