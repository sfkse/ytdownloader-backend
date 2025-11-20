import argparse
import os
import sys
import subprocess
from pathlib import Path
import yt_dlp


def check_ffmpeg():
    """Check if ffmpeg is available"""
    try:
        subprocess.run(["ffmpeg", "-version"], capture_output=True, check=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def download_video(url, output_path=None, return_file_path=False):
    """
    Download a YouTube video

    Args:
        url: YouTube video URL
        output_path: Output directory (default: Downloads folder for CLI, temp for API)
        return_file_path: If True, returns the file path instead of just success status

    Returns:
        If return_file_path=True: (success: bool, file_path: str or None)
        If return_file_path=False: success: bool
    """
    if not url or not url.strip():
        print("Error: Please provide a valid YouTube URL", file=sys.stderr)
        return (False, None) if return_file_path else False

    # Get Downloads folder path if not specified (for CLI usage)
    # For API usage, use temp directory
    if output_path is None:
        if return_file_path:
            # For API: use temp directory
            import tempfile

            downloads_path = tempfile.gettempdir()
        else:
            # For CLI: use user's Downloads folder
            downloads_path = str(Path.home() / "Downloads")
    else:
        downloads_path = output_path

    print(f"Downloading video from: {url}")
    print(f"Output directory: {downloads_path}")
    print("Downloading...")

    downloaded_file_path = None
    actual_downloaded_file = None

    try:
        # Track the actual downloaded file using progress hook
        def progress_hook(d):
            nonlocal actual_downloaded_file
            if d["status"] == "finished":
                actual_downloaded_file = d.get("filename")

            # Configure yt-dlp options

        # Use temp file pattern that yt-dlp will fill in
        # Prioritize quality over format - download best video+audio, then convert to MP4
        ydl_opts = {
            # Quality-first format selector - don't restrict by extension
            "format": "bestvideo[height>=1080]+bestaudio/bestvideo[height>=720]+bestaudio/bestvideo+bestaudio/best[height>=1080]/best[height>=720]/best[protocol!=m3u8]/best",
            "outtmpl": os.path.join(downloads_path, "%(title)s.%(ext)s"),
            "quiet": False,  # Show progress
            "progress_hooks": [progress_hook],
            "noplaylist": True,
            # Try to bypass bot detection
            "extractor_args": {
                "youtube": {
                    "player_client": ["tv_embedded", "ios", "android", "web"],
                    "skip": [
                        "dash",
                        "hls",
                    ],  # Skip adaptive formats that might trigger detection
                }
            },
            # Add more realistic headers
            "http_headers": {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
                "Accept-Language": "en-US,en;q=0.9",
                "Accept-Encoding": "gzip, deflate, br",
                "Referer": "https://www.youtube.com/",
            },
            # Retry on errors
            "retries": 3,
            "fragment_retries": 3,
        }

        # Use ffmpeg for post-processing to ensure highest quality and QuickTime compatibility
        print(f"Downloading with format selector: {ydl_opts.get('format', 'default')}")
        if check_ffmpeg():
            ydl_opts["postprocessors"] = [
                {
                    "key": "FFmpegVideoRemuxer",
                    "preferedformat": "mp4",
                }
            ]
            print(
                "Note: Using ffmpeg for post-processing to ensure highest quality and QuickTime compatibility"
            )
        else:
            # Fallback: try to get MP4 directly if ffmpeg is not available
            ydl_opts["format"] = (
                "best[ext=mp4][protocol!=m3u8]/best[protocol!=m3u8]/best[ext=mp4]/best"
            )
            print(
                "Warning: ffmpeg not available. Video quality may be limited to available MP4 formats."
            )

        # Download the video
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        # Use the actual downloaded file path from progress hook
        if actual_downloaded_file and os.path.exists(actual_downloaded_file):
            downloaded_file_path = actual_downloaded_file
        else:
            # Fallback: find the most recently created file in the downloads directory
            # Get video info to help identify the file
            with yt_dlp.YoutubeDL({"quiet": True}) as ydl:
                info = ydl.extract_info(url, download=False)
                title = info.get("title", "video")
                ext = info.get("ext", "mp4")

            # Find files matching the pattern (yt-dlp may sanitize the filename)
            import glob
            import time

            # Get all files in the directory
            all_files = [
                f
                for f in os.listdir(downloads_path)
                if os.path.isfile(os.path.join(downloads_path, f))
            ]

            # Filter files that might be our video (check by extension and recent modification)
            video_extensions = [".mp4", ".webm", ".mkv", ".m4a"]
            potential_files = [
                os.path.join(downloads_path, f)
                for f in all_files
                if any(f.lower().endswith(ext) for ext in video_extensions)
            ]

            # Sort by modification time, get the most recent
            if potential_files:
                potential_files.sort(key=lambda x: os.path.getmtime(x), reverse=True)
                # Get the most recently modified file (within last 5 minutes)
                most_recent = potential_files[0]
                if time.time() - os.path.getmtime(most_recent) < 300:  # 5 minutes
                    downloaded_file_path = most_recent

        if not downloaded_file_path or not os.path.exists(downloaded_file_path):
            raise FileNotFoundError(
                f"Downloaded file not found. Expected in: {downloads_path}"
            )

        print(f"\n✓ Download complete! Video saved to: {downloaded_file_path}")

        if not check_ffmpeg():
            print(
                "\n⚠ Note: ffmpeg is not installed. If the video doesn't play in QuickTime,"
            )
            print("   install ffmpeg with: brew install ffmpeg")
            print(
                "   This will ensure proper MP4 remuxing for QuickTime compatibility."
            )

        if return_file_path:
            return (True, downloaded_file_path)
        return True

    except Exception as e:
        print(f"\n✗ Download failed: {e}", file=sys.stderr)
        if return_file_path:
            return (False, None)
        return False


def main():
    parser = argparse.ArgumentParser(
        description="Download YouTube videos from command line"
    )
    parser.add_argument("url", help="YouTube video URL to download")
    parser.add_argument(
        "-o",
        "--output",
        dest="output_path",
        help="Output directory (default: ~/Downloads)",
    )

    args = parser.parse_args()

    success = download_video(args.url, args.output_path)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
