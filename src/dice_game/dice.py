import random
from typing import Protocol


class Roller(Protocol):
    def roll(self) -> int: ...


class RandomRoller:
    def roll(self):
        # TODO: Is this thread-safe?
        return random.randint(1, 6)
