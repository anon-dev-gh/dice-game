# Dice Game

## Build the image
docker buildx build -t an0ndev/dice-game:latest --target prod -f docker/Dockerfile .

## Publish
docker push an0ndev/dice-game:latest

## Start the game
docker run --rm --entrypoint python an0ndev/dice-game:latest src/dice_game/cli/server.py --host 0.0.0.0 --port 8765

## Join the game
docker run -it --rm --entrypoint python an0ndev/dice-game:latest src/dice_game/cli/client.py --host host.docker.internal --port 8765 --player-id 1 --player-name Alice
docker run --rm --entrypoint python an0ndev/dice-game:latest src/dice_game/cli/clien.py --host host.docker.internal --port 8765 --player-id 1 --player-name Alice