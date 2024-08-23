from collections import defaultdict
from typing import Callable, Dict, List, Type, TypeVar

from .events import Event

# Define a generic type variable for events
E = TypeVar("E", bound=Event)


class EventDispatcher:
    def __init__(self) -> None:
        self._handlers: Dict[Type[Event], List[Callable[[Event], None]]] = defaultdict(
            list
        )

    def register_handler(self, event_type: Type[E], handler: Callable[[E], None]):
        self._handlers[event_type].append(handler)  # type: ignore

    def dispatch(self, event: Event):
        for handler in self._handlers[type(event)]:
            handler(event)  # type: ignore
