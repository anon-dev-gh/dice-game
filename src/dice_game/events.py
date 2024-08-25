from dataclasses import dataclass


@dataclass
class Event:
    pass


@dataclass
class GameStartsEvent(Event):
    pass


@dataclass
class PlayerJoinsEvent(Event):
    player_id: int
    player_name: str


@dataclass
class PlayerRollsEvent(Event):
    player_id: int
    roll_result: int


@dataclass
class TurnFinishedEvent(Event):
    player_id: int
    score: int


@dataclass
class GameOverEvent(Event):
    winner_id: int
    winner_score: int
