import argparse
import asyncio

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


def start_server(host: str, port: int):
    async def main():
        # Set up the dispatcher and handlers
        dispatcher = EventDispatcher()
        dispatcher.register_handler(PlayerJoinsEvent, handle_player_joins)
        dispatcher.register_handler(PlayerRollsEvent, handle_player_rolls)
        dispatcher.register_handler(TurnFinishedEvent, handle_turn_finished)
        dispatcher.register_handler(GameOverEvent, handle_game_over)

        # Set up the game
        game = DiceGame(dispatcher)

        # Set up the WebSocket server
        websocket_server = WebSocketServer(
            host=host, port=port, game=game, dispatcher=dispatcher
        )

        # Start the WebSocket server
        await websocket_server.start()

    asyncio.run(main())


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Start the WebSocket game server.")
    parser.add_argument(
        "--host", type=str, default="localhost", help="The host to run the server on."
    )
    parser.add_argument(
        "--port", type=int, default=8765, help="The port to run the server on."
    )

    args = parser.parse_args()
    start_server(args.host, args.port)
