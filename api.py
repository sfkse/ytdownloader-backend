from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import sys
import logging
import os
import tempfile
from main import download_video

# Configure logging
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()
logging.basicConfig(
    level=getattr(logging, LOG_LEVEL, logging.INFO),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

app = Flask(__name__)
# CORS configuration - allow production frontend domain
CORS_ORIGINS = os.getenv(
    "CORS_ORIGINS",
    "https://ytdownload.help,http://localhost:3000,http://127.0.0.1:3000",
).split(",")
CORS(app, origins=CORS_ORIGINS)  # Enable CORS for frontend requests


@app.route("/api/download", methods=["POST", "OPTIONS"])
def download():
    """API endpoint to download YouTube videos and stream to user's browser"""
    logger.info(f"Received request: {request.method} {request.path}")
    logger.info(f"Headers: {dict(request.headers)}")

    if request.method == "OPTIONS":
        return jsonify({"status": "ok"}), 200

    downloaded_file_path = None
    try:
        data = request.get_json()
        logger.info(f"Request data: {data}")

        if not data or "url" not in data:
            return jsonify({"error": "URL is required"}), 400

        url = data["url"].strip()

        if not url:
            return jsonify({"error": "URL cannot be empty"}), 400

        # Validate YouTube URL
        if "youtube.com" not in url and "youtu.be" not in url:
            return jsonify({"error": "Please provide a valid YouTube URL"}), 400

        # Download the video to temp directory and get file path
        success, downloaded_file_path = download_video(url, return_file_path=True)

        if not success or not downloaded_file_path:
            return (
                jsonify(
                    {
                        "error": "Download failed. Please check the URL and try again.",
                        "success": False,
                    }
                ),
                500,
            )

        # Verify file exists
        if not os.path.exists(downloaded_file_path):
            logger.error(f"Downloaded file not found: {downloaded_file_path}")
            return (
                jsonify({"error": "File was downloaded but not found on server"}),
                500,
            )

        # Get filename for download
        filename = os.path.basename(downloaded_file_path)

        # Stream the file to the user's browser
        # This will trigger a download in the user's Downloads folder
        response = send_file(
            downloaded_file_path,
            as_attachment=True,
            download_name=filename,
            mimetype="video/mp4",
        )

        # Schedule file cleanup after response is sent
        # Note: In production, you might want to use a background task queue
        # For now, we'll clean up after a delay
        def cleanup_file(file_path):
            import time

            time.sleep(60)  # Wait 60 seconds before cleanup
            try:
                if os.path.exists(file_path):
                    os.remove(file_path)
                    logger.info(f"Cleaned up temporary file: {file_path}")
            except Exception as e:
                logger.warning(f"Failed to cleanup file {file_path}: {e}")

        import threading

        cleanup_thread = threading.Thread(
            target=cleanup_file, args=(downloaded_file_path,)
        )
        cleanup_thread.daemon = True
        cleanup_thread.start()

        return response

    except Exception as e:
        logger.error(f"Error in download endpoint: {str(e)}", exc_info=True)
        # Clean up file if it exists
        if downloaded_file_path and os.path.exists(downloaded_file_path):
            try:
                os.remove(downloaded_file_path)
            except:
                pass
        return jsonify({"error": str(e), "success": False}), 500


@app.route("/", methods=["GET"])
def root():
    """Root endpoint"""
    return jsonify({"message": "YouTube Downloader API", "status": "running"}), 200


@app.route("/health", methods=["GET"])
def health():
    """Health check endpoint"""
    logger.info("Health check requested")
    return jsonify({"status": "ok"}), 200


@app.before_request
def log_request_info():
    """Log incoming requests"""
    logger.info(f"Request: {request.method} {request.path}")
    logger.info(f"Headers: {dict(request.headers)}")


if __name__ == "__main__":
    # Production settings
    port = int(os.getenv("PORT", 8080))
    debug = os.getenv("FLASK_DEBUG", "False").lower() == "true"
    app.run(host="0.0.0.0", port=port, debug=debug)
