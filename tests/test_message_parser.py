from dice_game.events import PlayerJoinsEvent, PlayerRollsEvent, TurnFinishedEvent, GameOverEvent
from dice_game.message_parser import PlayerJoinsEventSerde, PlayerRollsEventSerde, TurnFinishedEventSerde, GameOverEventSerde

def test_player_joins_event_serde():
    event = PlayerJoinsEvent(player_id="1", player_name="Alice")
    serialized = {
        "event": "join",
        "player_id": "1",
        "player_name": "Alice"
    }
    serde = PlayerJoinsEventSerde()
    assert serde.serialize(event) == serialized
    assert serde.deserialize(serialized) == event

def test_player_rolls_event_serde():
    event = PlayerRollsEvent(player_id="1", roll_result=5)
    serialized = {
        "event": "roll",
        "player_id": "1",
        "roll_result": 5
    }
    serde = PlayerRollsEventSerde()
    assert serde.serialize(event) == serialized
    assert serde.deserialize(serialized) == event

def test_turn_finished_event_serde():
    event = TurnFinishedEvent(player_id="1", score=10)
    serialized = {
        "event": "finish_turn",
        "player_id": "1",
        "score": 10
    }
    serde = TurnFinishedEventSerde()
    assert serde.serialize(event) == serialized
    assert serde.deserialize(serialized) == event

def test_game_over_event_serde():
    event = GameOverEvent(winner_id="1", winner_score=100)
    serialized = {
        "event": "end_game",
        "winner_id": "1",
        "winner_score": 100
    }
    serde = GameOverEventSerde()
    assert serde.serialize(event) == serialized
    assert serde.deserialize(serialized) == event


