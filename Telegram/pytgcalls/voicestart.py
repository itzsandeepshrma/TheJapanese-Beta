import logging
import os
import time
from pytgcalls import Client as TgCallsClient
from pyrogram import Client, filters
from pyrogram.types import Message
from dotenv import load_dotenv
from datetime import datetime

# Load environment variables securely
load_dotenv()

API_ID = os.getenv('API_ID')
API_HASH = os.getenv('API_HASH')
AUTHORIZED_USERS = list(map(int, os.getenv('AUTHORIZED_USERS').split(',')))
RATE_LIMIT_TIME = 10  # Rate limit in seconds

# Setup detailed logging for debugging and error tracking
logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# Create the bot client
bot = Client("YourBot", api_id=API_ID, api_hash=API_HASH)

# Initialize the group call client
tg_calls = TgCallsClient("call_session")

# Track last command usage time for rate limiting
last_used = {}

# Helper function to verify if the user is authorized
def is_authorized(user_id):
    return user_id in AUTHORIZED_USERS

# Helper function for rate limiting
def check_rate_limit(user_id):
    global last_used
    current_time = time.time()
    if user_id in last_used:
        elapsed_time = current_time - last_used[user_id]
        if elapsed_time < RATE_LIMIT_TIME:  # Rate limit exceeded
            return False
    last_used[user_id] = current_time
    return True

# Command to start voice playback in a group call
@bot.on_message(filters.command("voicestart"))
async def start_voice(client, message: Message):
    if not is_authorized(message.from_user.id):
        logger.warning(f"Unauthorized voice start attempt by user {message.from_user.id} at {datetime.now()}")
        await message.reply("You are not authorized to start the voice playback!")
        return

    if not check_rate_limit(message.from_user.id):
        logger.info(f"Rate limit exceeded for user {message.from_user.id} at {datetime.now()}")
        await message.reply("You are using commands too frequently. Please try again later.")
        return

    voice_url = message.text.split(" ", 1)[-1].strip()  # Extract the voice URL from the command

    if not voice_url:
        await message.reply("Please provide a valid voice URL to play!")
        return

    try:
        logger.info(f"User {message.from_user.id} is attempting to start voice playback: {voice_url} at {datetime.now()}")
        
        # Start playing the voice in the group call
        await tg_calls.play_audio(message.chat.id, voice_url)
        logger.info(f"User {message.from_user.id} successfully started the voice playback at {datetime.now()}")
        await message.reply(f"Now playing the voice: {voice_url}")
    except Exception as e:
        logger.error(f"Error occurred for user {message.from_user.id} while starting voice playback: {e}")
        await message.reply("Failed to start the voice playback. Please check the URL or try again later.")

# Enhanced error handling for bot runtime
if __name__ == "__main__":
    try:
        bot.run()
    except Exception as e:
        logger.critical(f"Critical error encountered while running the bot: {e}")
