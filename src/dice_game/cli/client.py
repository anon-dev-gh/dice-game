# src/dice_game/cli_client.py

import argparse
import asyncio
import json

import websockets


async def send_message(websocket, message):
    await websocket.send(json.dumps(message))


async def receive_message(websocket):
    response = await websocket.recv()
    return json.loads(response)


async def start_client(uri, player_id, player_name):
    async with websockets.connect(uri) as websocket:
        # Join the game
        await send_message(
            websocket,
            {"event": "join", "player_id": player_id, "player_name": player_name},
        )

        print(f"Joined the game as {player_name} (ID: {player_id})")

        # Main loop to interact with the server
        while True:
            print("\nChoose an action:")
            print("1. Roll Dice")
            print("2. Finish Turn")
            print("3. End Game")
            print("4. Quit")
            choice = input("Enter your choice: ")

            if choice == "1":
                await send_message(websocket, {"event": "roll", "player_id": player_id})
                response = await receive_message(websocket)
                print(f"Roll result: {response['roll_result']}")

            elif choice == "2":
                await send_message(
                    websocket, {"event": "finish_turn", "player_id": player_id}
                )
                print("Turn finished.")

            elif choice == "3":
                await send_message(
                    websocket, {"event": "end_game", "player_id": player_id}
                )
                print("Game ended.")
                break

            elif choice == "4":
                print("Quitting the game.")
                break

            else:
                print("Invalid choice. Please try again.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Connect to the WebSocket game server."
    )
    parser.add_argument(
        "--host", type=str, default="localhost", help="The server host to connect to."
    )
    parser.add_argument(
        "--port", type=int, default=8765, help="The server port to connect to."
    )
    parser.add_argument("--player-id", type=int, required=True, help="Your player ID.")
    parser.add_argument(
        "--player-name", type=str, required=True, help="Your player name."
    )

    args = parser.parse_args()
    uri = f"ws://{args.host}:{args.port}"

    asyncio.run(start_client(uri, args.player_id, args.player_name))
