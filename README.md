# YouTube Downloader - Backend API

Flask-based REST API for downloading YouTube videos. The API downloads videos server-side and streams them to users' browsers, saving files to their local Downloads folder.

## 🚀 Features

- Download YouTube videos in best quality MP4 format
- Stream videos directly to user's browser
- Automatic file cleanup after download
- CORS support for frontend integration
- Health check endpoint for monitoring

## 📋 Prerequisites

- Python 3.8+
- pip or pip3
- ffmpeg (optional, for better video compatibility)

## 🛠️ Installation

1. Clone the repository:
```bash
git clone https://github.com/sfkse/ytdownloader-backend.git
cd ytdownloader-backend
```

2. Create a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. (Optional) Install ffmpeg for better video compatibility:
```bash
# macOS
brew install ffmpeg

# Ubuntu/Debian
sudo apt-get install ffmpeg

# Windows
# Download from https://ffmpeg.org/download.html
```

## ⚙️ Configuration

Create a `.env` file in the root directory:

```env
PORT=8080
FLASK_DEBUG=False
LOG_LEVEL=INFO
CORS_ORIGINS=https://ytdownload.help,http://localhost:3000
```

### Environment Variables

- `PORT` - Server port (default: 8080)
- `FLASK_DEBUG` - Enable debug mode (default: False)
- `LOG_LEVEL` - Logging level: DEBUG, INFO, WARNING, ERROR (default: INFO)
- `CORS_ORIGINS` - Comma-separated list of allowed origins for CORS

## 🏃 Running the Server

### Development Mode

```bash
python api.py
```

Or use the startup script:
```bash
./start_server.sh
```

### Production Mode

Using Gunicorn (recommended):
```bash
gunicorn -c gunicorn_config.py api:app
```

Or with custom settings:
```bash
gunicorn -w 4 -b 0.0.0.0:8080 --timeout 600 api:app
```

## 📡 API Endpoints

### POST /api/download
Download a YouTube video and stream it to the client.

**Request:**
```json
{
  "url": "https://www.youtube.com/watch?v=VIDEO_ID"
}
```

**Response:**
- Success: Video file stream (triggers browser download)
- Error: JSON error message

### GET /health
Health check endpoint.

**Response:**
```json
{
  "status": "ok"
}
```

### GET /
Root endpoint.

**Response:**
```json
{
  "message": "YouTube Downloader API",
  "status": "running"
}
```

## 🏗️ Project Structure

```
ytdownloader-backend/
├── api.py                 # Flask application and API routes
├── main.py                # Core download logic
├── gunicorn_config.py     # Gunicorn configuration for production
├── requirements.txt       # Python dependencies
├── start_server.sh        # Startup script
├── .env.example           # Environment variables template
└── README.md              # This file
```

## 🚢 Deployment

See [DEPLOYMENT.md](./DEPLOYMENT.md) for detailed deployment instructions.

### Quick Deploy Checklist

1. Set up environment variables (`.env`)
2. Install dependencies
3. Configure CORS origins
4. Set up reverse proxy (Nginx)
5. Configure SSL certificates
6. Start with Gunicorn or systemd service

## 🔒 Security Considerations

- Videos are downloaded to temporary directory and cleaned up after 60 seconds
- CORS is configured to only allow requests from specified origins
- Input validation for YouTube URLs
- Consider adding rate limiting for production use

## 📝 License

[Add your license here]

## 🤝 Contributing

[Add contribution guidelines here]

## 📧 Support

For issues and questions, please open an issue on GitHub.

