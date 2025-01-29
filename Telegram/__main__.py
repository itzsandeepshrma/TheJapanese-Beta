import os
import logging
from pyrogram import Client, filters
from pyrogram.types import Message
from pytgcalls import Client as TgCallsClient
from yt_dlp import YoutubeDL
import tempfile
from dotenv import load_dotenv
import sys

# Load environment variables
load_dotenv()

# Setup logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger()

# Fetch API keys and tokens from environment variables
API_ID = os.getenv("API_ID")
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Check for missing environment variables
missing_vars = [var for var in ["API_ID", "API_HASH", "BOT_TOKEN"] if not os.getenv(var)]
if missing_vars:
    for var in missing_vars:
        logger.error(f"Missing environment variable: {var}")
    sys.exit(1)

# Initialize bot client
bot = Client("The-Japanese-Bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)
tg_calls = TgCallsClient("call_session")

# Function to search and download the song
def search_and_download_song(query):
    try:
        logger.info(f"Searching for song: {query}")
        
        ydl_opts = {
            'format': 'bestaudio/best',
            'noplaylist': True,
            'quiet': True,
            'outtmpl': tempfile.mktemp()  # Temporary file
        }
        
        with YoutubeDL(ydl_opts) as ydl:
            result = ydl.extract_info(f"ytsearch:{query}", download=True)
            song_url = result['entries'][0]['url']
            logger.info(f"Song found: {query}")
            return song_url
    except Exception as e:
        logger.error(f"Error downloading song: {e}")
        return None

# Command to greet users
async def greet_user(client: Client, message: Message):
    await message.reply("Hello, welcome to The-Japanese Bot! How can I assist you today?")

# Command to echo messages
async def echo(client: Client, message: Message):
    await message.reply(message.text)

# Command: /start
@bot.on_message(filters.command("start"))
async def handle_start(client: Client, message: Message):
    await greet_user(client, message)

# Command: /play <song name>
@bot.on_message(filters.command("play"))
async def play_user_song(client, message):
    try:
        query = message.text.split(" ", 1)[1]  # Get song name
        song_url = search_and_download_song(query)
        
        if song_url:
            await tg_calls.join_group_call(message.chat.id, song_url)
            await message.reply(f"Now playing: {query}")
        else:
            await message.reply("Failed to find or download the song. Please try again.")
    except IndexError:
        await message.reply("Please provide a song name after /play.")
    except Exception as e:
        logger.error(f"Error in /play command: {e}")
        await message.reply(f"Error: {e}")

# Handle all text messages
@bot.on_message(filters.text)
async def handle_text(client: Client, message: Message):
    await echo(client, message)

# Start the bot
if __name__ == "__main__":
    try:
        logger.info("Starting The-Japanese Bot...")
        bot.run()
    except KeyboardInterrupt:
        logger.info("Bot stopped by user.")
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        sys.exit(1)
