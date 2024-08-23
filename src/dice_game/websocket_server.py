import asyncio
import json
from typing import MutableMapping

import websockets

from dice_game.dispatcher import EventDispatcher
from dice_game.events import Event, PlayerJoinsEvent, PlayerRollsEvent
from dice_game.game import DiceGame
from dice_game.message_parser import MessageParser


class WebSocketServer:
    def __init__(
        self, host: str, port: int, game: DiceGame, dispatcher: EventDispatcher
    ):
        self.host = host
        self.port = port
        self.game = game
        self.dispatcher = dispatcher
        self.connections: MutableMapping[int, websockets.WebSocketServerProtocol] = {}
        self.parser = MessageParser()

    async def handler(self, websocket, path):
        # Handle a new player connection
        async for message in websocket:
            event = self.parser.parse_message(message)
            if event:
                await self.dispatch_event(event, websocket)

    async def dispatch_event(self, event: Event, websocket):
        # Dispatch the event and manage WebSocket-specific logic
        self.dispatcher.dispatch(event)

        # Special handling based on event type
        if isinstance(event, PlayerJoinsEvent):
            self.connections[event.player_id] = websocket

        elif isinstance(event, PlayerRollsEvent):
            await self.send_message(
                event.player_id,
                {
                    "event": "roll_result",
                    "player_id": event.player_id,
                    "roll_result": event.roll_result,
                },
            )

    async def send_message(self, player_id: int, message: dict):
        websocket = self.connections.get(player_id)
        if websocket:
            await websocket.send(json.dumps(message))

    async def broadcast(self, message: dict):
        if self.connections:
            tasks = [
                asyncio.create_task(ws.send(json.dumps(message)))
                for ws in self.connections.values()
            ]
            await asyncio.wait(tasks)

    async def start(self):
        async with websockets.serve(self.handler, self.host, self.port):
            print(f"WebSocket server started on ws://{self.host}:{self.port}")
            await asyncio.Future()  # run forever
