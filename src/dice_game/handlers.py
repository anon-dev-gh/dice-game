from dice_game.events import (
    GameOverEvent,
    PlayerJoinsEvent,
    PlayerRollsEvent,
    TurnFinishedEvent,
)
from dice_game.game import DiceGame


def handle_player_joins(game: DiceGame, event: PlayerJoinsEvent) -> None:
    print(f"Player {event.player_name} with ID {event.player_id} has joined the game.")


def handle_player_rolls(game: DiceGame, event: PlayerRollsEvent) -> None:
    print(f"Player {event.player_id} rolled a {event.roll_result}.")


def handle_turn_finished(game: DiceGame, event: TurnFinishedEvent) -> None:
    print(
        f"Player {event.player_id} finished their turn with a score of {event.score}."
    )


def handle_game_over(game: DiceGame, event: GameOverEvent) -> None:
    print(
        f"Game over! Player {event.winner_id} won with a score of {event.winner_score}."
    )
