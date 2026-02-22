#!/usr/bin/env bash

# Set strict error handling
set -euo pipefail

echo "🚀 Loading Python environment..."

# Check if 'uv' is installed
if ! command -v uv >/dev/null 2>&1; then
    echo -e "📦 'uv' not installed. Installing..."
    curl -LsSf https://astral.sh/uv/install.sh | sh || {
        echo -e "❌ Failed to install uv."
        return 1
    }
    source "$HOME/.cargo/env"
fi

echo -e "🛠️ Creating virtual environment..."
if ! uv venv; then
    echo -e "❌ Failed to create virtual environment."
    return 1
fi

if ! source .venv/bin/activate; then
    echo -e "❌ Failed to activate virtual environment."
    return 1
fi

echo -e "🔄 Syncing dependencies..."
if ! uv sync ; then
    echo -e "❌ Failed to sync dependencies."
    return 1
fi

echo "✅ Environment setup complete!"
