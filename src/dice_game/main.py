# src/main.py

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
        host="localhost", port=8765, game=game, dispatcher=dispatcher
    )

    # Start the WebSocket server and the game
    await websocket_server.start()


if __name__ == "__main__":
    asyncio.run(main())
