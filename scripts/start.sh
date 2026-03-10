#!/usr/bin/env bash

# Set strict error handling
set -euo pipefail

# cd into the parent directory of the script,
# so that the script generates virtual environments always in the same path.
cd "${0%/*}" || exit 1

cd ../

# Load env
# ./scripts/load_python_env.sh


# Build frontend
echo "🚀 Starting Vite Dev frontend..."
cd ./app/frontend

# Install dependencies if needed
# npm install

# Start frontend in background
npm run dev -- --host 0.0.0.0 --port 5173 &
FRONTEND_PID=$!


# Build backend
echo "🚀 Starting backend..."
cd ../backend

port=8000
host=127.0.0.1
uvicorn "main:app" --host "$host" --port "$port" --reload &
BACKEND_PID=$!

wait $FRONTEND_PID $BACKEND_PID
