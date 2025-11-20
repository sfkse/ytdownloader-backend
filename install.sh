#!/bin/bash
# YouTube Downloader - Quick Install Script

set -e

echo "🎬 YouTube Downloader - Installation"
echo "===================================="
echo ""

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required but not installed."
    echo "   Please install Python 3.8+ and try again."
    exit 1
fi

echo "✓ Python found: $(python3 --version)"

# Create venv
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
else
    echo "✓ Virtual environment already exists"
fi

# Activate venv
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📥 Installing dependencies..."
pip install --upgrade pip --quiet
pip install -r requirements.txt --quiet

# Check ffmpeg
if command -v ffmpeg &> /dev/null; then
    echo "✓ ffmpeg found: $(ffmpeg -version | head -n 1 | cut -d' ' -f1-3)"
else
    echo "⚠️  ffmpeg not found (optional but recommended for best quality)"
    echo "   Install with:"
    echo "   - macOS: brew install ffmpeg"
    echo "   - Ubuntu/Debian: sudo apt-get install ffmpeg"
    echo "   - Windows: Download from https://ffmpeg.org/download.html"
fi

echo ""
echo "✅ Installation complete!"
echo ""
echo "🚀 To start the server, run:"
echo "   ./start.sh"
echo ""
echo "   Or manually:"
echo "   source venv/bin/activate"
echo "   python api.py"
echo ""

