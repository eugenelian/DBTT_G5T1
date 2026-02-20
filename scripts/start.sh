#!/usr/bin/env bash

# Set strict error handling
set -euo pipefail

# cd into the parent directory of the script,
# so that the script generates virtual environments always in the same path.
cd "${0%/*}" || exit 1

cd ../

# ./scripts/load_python_env.sh

cd ./app/frontend

# TODO: Build frontend

echo "🚀 Starting backend..."

cd ../backend

port=8000
host=127.0.0.1
uvicorn "main:app" --host "$host" --port "$port" --reload
out=$?
if [ $out -ne 0 ]; then
    echo "❌ Failed to start backend"
    exit $out
fi
