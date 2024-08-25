import asyncio
from functools import partial

from dice_game.dispatcher import EventDispatcher
from dice_game.events import (
    GameOverEvent,
    PlayerJoinsEvent,
    PlayerRollsEvent,
    TurnFinishedEvent,
)
from dice_game.game import DiceGame
from dice_game.handlers import (
    handle_game_over,
    handle_player_joins,
    handle_player_rolls,
    handle_turn_finished,
)
from dice_game.websocket_server import WebSocketServer


async def start_server(host: str, port: int):
    # Initialize the game
    game = DiceGame()

    # Set up the dispatcher and handlers
    dispatcher = EventDispatcher()
    dispatcher.register_handler(PlayerJoinsEvent, partial(handle_player_joins, game))
    dispatcher.register_handler(PlayerRollsEvent, partial(handle_player_rolls, game))
    dispatcher.register_handler(TurnFinishedEvent, partial(handle_turn_finished, game))
    dispatcher.register_handler(GameOverEvent, partial(handle_game_over, game))

    # Set up the WebSocket server
    websocket_server = WebSocketServer(
        host=host, port=port, game=game, dispatcher=dispatcher
    )

    # Start the WebSocket server and the game
    await websocket_server.start()


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Start the WebSocket game server.")
    parser.add_argument(
        "--host", type=str, default="localhost", help="The host to run the server on."
    )
    parser.add_argument(
        "--port", type=int, default=8765, help="The port to run the server on."
    )

    args = parser.parse_args()

    asyncio.run(start_server(args.host, args.port))
