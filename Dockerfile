# Use an official Python 3.12 runtime as a parent image
FROM python:3.12-slim

# Set environment variables consistently
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    UV_PROJECT_ENVIRONMENT="/usr/local/" \
    # Ensure scripts know where the app root is
    PYTHONPATH="/app"

# Install uv package manager
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /usr/local/bin/

# Set the working directory in the container
WORKDIR /app

# Install curl (for healthchecks), CA certificates for TLS + Proper Certificate Validation and clean up
RUN apt-get update && \
    apt-get install -y --no-install-recommends curl ca-certificates && \
    update-ca-certificates && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Copy and install dependencies first for caching efficiency
COPY pyproject.toml uv.lock* ./
RUN uv sync --no-dev --frozen --no-cache

# Copy the rest of the application code
COPY . /app

# Ensure scripts (if present) are executable
RUN chmod +x scripts/* || true

# Switch to non-root user (best practice)
RUN useradd -ms /bin/bash appuser
USER appuser

WORKDIR /app/app/backend

# Make port 8000 available (adjust if your API uses a different port)
EXPOSE 8000

# Default command (removed --reload in production)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
