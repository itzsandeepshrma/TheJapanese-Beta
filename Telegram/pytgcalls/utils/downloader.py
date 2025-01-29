import os
import tempfile
from yt_dlp import YoutubeDL

def download_song(query: str):
    """
    Search and download a song from YouTube.
    :param query: The name of the song to search for.
    :return: The path to the downloaded song or None if failed.
    """
    try:
        ydl_opts = {
            "format": "bestaudio/best",
            "noplaylist": True,
            "quiet": True,
            "outtmpl": tempfile.mktemp(suffix=".mp3")  # Save as a temporary file
        }
        with YoutubeDL(ydl_opts) as ydl:
            result = ydl.extract_info(f"ytsearch:{query}", download=True)
            song_path = ydl.prepare_filename(result["entries"][0])
            return song_path
    except Exception as e:
        print(f"Error downloading song: {e}")
        return None
