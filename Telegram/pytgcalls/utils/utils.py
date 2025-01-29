import os
from yt_dlp import YoutubeDL
import tempfile
import logging
from pytgcalls import Client as TgCallsClient

# Initialize logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# Initialize TgCallsClient
tg_calls = TgCallsClient("call_session")

# Function to search and download the song
def search_and_download_song(query):
    try:
        # Log the search query
        logger.info(f"Searching for song: {query}")
        
        # Using yt-dlp to download the song
        ydl_opts = {
            'format': 'bestaudio/best',
            'noplaylist': True,
            'quiet': True,
            'outtmpl': tempfile.mktemp()  # Temporary file
        }
        
        with YoutubeDL(ydl_opts) as ydl:
            result = ydl.extract_info(f"ytsearch:{query}", download=True)
            song_url = result['entries'][0]['url']  # Get the URL of the song

            # Log successful search
            logger.info(f"Song found: {query}")
            return song_url
    except Exception as e:
        logger.error(f"Error downloading song: {e}")
        return None

# Function to play the song in a group call
def play_song_in_call(chat_id, song_url):
    try:
        tg_calls.join_group_call(chat_id, song_url)
        logger.info(f"Song played in chat: {chat_id}")
    except Exception as e:
        logger.error(f"Error playing song: {e}")
        return False
    return True
