#!/bin/bash

# Navigate to the project directory
cd "$(dirname "$0")"

# Activate virtual environment
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
    source venv/bin/activate
    echo "Installing dependencies..."
    pip install -r requirements.txt
else
    source venv/bin/activate
fi

# Load environment variables if .env exists
if [ -f .env ]; then
    export $(cat .env | grep -v '^#' | xargs)
fi

# Check if running in production mode
if [ "$FLASK_ENV" = "production" ] || [ -n "$PORT" ]; then
    echo "Starting Flask server in production mode with Gunicorn..."
    if [ -f "gunicorn_config.py" ]; then
        gunicorn -c gunicorn_config.py api:app
    else
        gunicorn -w 4 -b 0.0.0.0:${PORT:-8080} --timeout 600 api:app
    fi
else
    # Development mode
    echo "Starting Flask server in development mode on http://127.0.0.1:8080"
    python api.py
fi

