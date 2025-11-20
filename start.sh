#!/bin/bash
# Simple start script for local development

cd "$(dirname "$0")"

# Activate venv
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found. Run ./install.sh first"
    exit 1
fi

source venv/bin/activate

# Start server
echo "🚀 Starting YouTube Downloader API..."
echo "📍 Server will be available at: http://localhost:8080"
echo "🛑 Press Ctrl+C to stop"
echo ""

python api.py

