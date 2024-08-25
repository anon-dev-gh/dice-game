from typing import Callable, Dict, List, Type

from dice_game.events import Event


class EventDispatcher:
    def __init__(self) -> None:
        self._handlers: Dict[Type[Event], List[Callable[[Event], None]]] = {}

    def register_handler(
        self, event_type: Type[Event], handler: Callable[[Event], None]
    ):
        if event_type not in self._handlers:
            self._handlers[event_type] = []
        self._handlers[event_type].append(handler)

    def dispatch(self, event: Event):
        event_type = type(event)
        if event_type in self._handlers:
            for handler in self._handlers[event_type]:
                handler(event)
