#!/usr/bin/env bash

# Set strict error handling
set -euo pipefail

./scripts/load_python_env.sh

echo "🚀 Running 'prepdocs.py' update..."

uv run python -m app.backend.prepdocslib.vector_store --function update

echo "✅ Finished running 'prepdocs.py' update."
