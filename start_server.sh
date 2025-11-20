#!/bin/bash
# Alternative startup script (same as start.sh)

cd "$(dirname "$0")"

if [ ! -d "venv" ]; then
    echo "Virtual environment not found. Run ./install.sh first"
    exit 1
fi

source venv/bin/activate

# Load environment variables if .env exists
if [ -f .env ]; then
    export $(cat .env | grep -v '^#' | xargs)
fi

echo "🚀 Starting YouTube Downloader API..."
echo "📍 Server will be available at: http://localhost:${PORT:-8080}"
echo "🛑 Press Ctrl+C to stop"
echo ""

python api.py

