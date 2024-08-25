from typing import Dict, Protocol, Type, TypeVar

from dice_game.events import (
    Event,
    GameOverEvent,
    PlayerJoinsEvent,
    PlayerRollsEvent,
    TurnFinishedEvent,
)

T = TypeVar("T", bound=Event)


class EventSerde(Protocol[T]):
    def serialize(self, event: T) -> Dict: ...

    def deserialize(self, serialized: Dict) -> T: ...


class EventSerdeRegistry:
    def __init__(self) -> None:
        self._serdes_by_str: Dict[str, EventSerde] = {}
        self._serdes_by_type: Dict[Type[Event], EventSerde] = {}

        # Each tuple contains (serde_instance, event_string, event_type)
        serdes: list[tuple[EventSerde, str, Type[Event]]] = [
            (PlayerJoinsEventSerde(), "join", PlayerJoinsEvent),
            (PlayerRollsEventSerde(), "roll", PlayerRollsEvent),
            (TurnFinishedEventSerde(), "finish_turn", TurnFinishedEvent),
            (GameOverEventSerde(), "game_over", GameOverEvent),
        ]

        for serde, event_str, event_type in serdes:
            self._serdes_by_str[event_str] = serde
            self._serdes_by_type[event_type] = serde

    def serialize(self, event: Event) -> Dict:
        event_type = type(event)
        if event_type not in self._serdes_by_type:
            raise ValueError(
                f"No serializer found for event type: {event_type.__name__}"
            )
        return self._serdes_by_type[event_type].serialize(event)

    def deserialize(self, serialized: Dict) -> Event:
        event_type = serialized.get("event")
        if not event_type:
            raise ValueError("event is expected")
        if event_type not in self._serdes_by_str:
            raise ValueError(f"No deserializer found for event type: {event_type}")
        return self._serdes_by_str[event_type].deserialize(serialized)


class PlayerJoinsEventSerde:
    def serialize(self, event: PlayerJoinsEvent) -> Dict:
        return {
            "event": "join",
            "player_id": event.player_id,
            "player_name": event.player_name,
        }

    def deserialize(self, serialized: Dict) -> PlayerJoinsEvent:
        return PlayerJoinsEvent(
            player_id=serialized["player_id"], player_name=serialized["player_name"]
        )


class PlayerRollsEventSerde:
    def serialize(self, event: PlayerRollsEvent) -> Dict:
        return {
            "event": "roll",
            "player_id": event.player_id,
            "roll_result": event.roll_result,
        }

    def deserialize(self, serialized: Dict) -> PlayerRollsEvent:
        return PlayerRollsEvent(
            player_id=serialized["player_id"], roll_result=serialized["roll_result"]
        )


class TurnFinishedEventSerde:
    def serialize(self, event: TurnFinishedEvent) -> Dict:
        return {
            "event": "finish_turn",
            "player_id": event.player_id,
            "score": event.score,
        }

    def deserialize(self, serialized: Dict) -> TurnFinishedEvent:
        return TurnFinishedEvent(
            player_id=serialized["player_id"], score=serialized["score"]
        )


class GameOverEventSerde:
    def serialize(self, event: GameOverEvent) -> Dict:
        return {
            "event": "end_game",
            "winner_id": event.winner_id,
            "winner_score": event.winner_score,
        }

    def deserialize(self, serialized: Dict) -> GameOverEvent:
        return GameOverEvent(
            winner_id=serialized["winner_id"], winner_score=serialized["winner_score"]
        )
