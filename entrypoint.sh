#!/bin/bash
set -e

MODE=$1
PORT=$2

if [ -z "$MODE" ] || [ -z "$PORT" ]; then
    echo "Usage: ./entrypoint.sh <mode> <port>"
    echo "Example: ./entrypoint.sh bad 5000"
    exit 1
fi

echo "Starting Vulpy in $MODE mode on port $PORT..."
cd $MODE

# Check if databases exist, if not run init
if [ ! -f "db_users.sqlite" ] || [ ! -f "db_posts.sqlite" ]; then
    echo "Initializing database..."
    python db_init.py
fi

# Run the application
# We use flask run to bind to 0.0.0.0
export FLASK_APP=vulpy.py
export FLASK_DEBUG=1
python -m flask run --host=0.0.0.0 --port=$PORT
