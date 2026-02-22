#!/usr/bin/env bash

# Set strict error handling
set -euo pipefail

./scripts/load_python_env.sh

echo "🚀 Running 'prepdocs.py' build..."

uv run python -m app.backend.prepdocslib.vector_store --function build

echo "✅ Finished running 'prepdocs.py' build."
