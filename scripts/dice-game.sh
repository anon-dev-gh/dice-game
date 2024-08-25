#!/bin/bash

export PYTHONPATH=/workspace/src:${PYTHONPATH}

if [ "$1" == "--server" ]; then
    shift
    python3 src/dice_game/cli/server.py "$@"
elif [ "$1" == "--client" ]; then
    shift
    python3 src/dice_game/cli/client.py "$@"
else
    echo "Usage: $0 --server [server-options] | --client [client-options]"
    exit 1
fi
