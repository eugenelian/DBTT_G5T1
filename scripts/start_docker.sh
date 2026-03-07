#!/usr/bin/env bash

# Set strict error handling
set -euo pipefail

COMPOSE_FILES="-f docker-compose.yaml"

cleanup() {
  echo ""
  echo "🛑 Shutting down Docker Compose..."
  docker compose $COMPOSE_FILES down
}

# Run cleanup on script exit (Ctrl+C, error, normal exit)
trap cleanup EXIT

echo "🚀 Starting Docker..."

docker compose $COMPOSE_FILES up --build -d

echo ""
echo "✔️ Started Docker successfully"
