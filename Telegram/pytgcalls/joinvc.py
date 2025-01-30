import logging
import os
import time
from pytgcalls import Client as TgCallsClient
from pyrogram import Client, filters
from pyrogram.types import Message
from dotenv import load_dotenv
from datetime import datetime

# Load environment variables for API credentials securely
load_dotenv()

API_ID = os.getenv('API_ID')
API_HASH = os.getenv('API_HASH')
AUTHORIZED_USERS = list(map(int, os.getenv('AUTHORIZED_USERS').split(',')))
RATE_LIMIT_TIME = 10  # Rate limit in seconds

# Setup logging for debugging and error tracking with enhanced info
logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# Create the bot client
bot = Client("YourBot", api_id=API_ID, api_hash=API_HASH)

# Initialize a group call client
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
        if elapsed_time < RATE_LIMIT_TIME:  # If user exceeds rate limit time
            return False
    last_used[user_id] = current_time
    return True

# Command to start the bot with logging
@bot.on_message(filters.command("start"))
async def start(client, message: Message):
    if not is_authorized(message.from_user.id):
        logger.warning(f"Unauthorized access attempt by user {message.from_user.id} at {datetime.now()}")
        await message.reply("You are not authorized to use this bot!")
        return

    logger.info(f"User {message.from_user.id} started the bot at {datetime.now()}")
    await message.reply("Bot Started! How can I assist you today?")

# Command to initiate a call with advanced error handling and logging
@bot.on_message(filters.command("call"))
async def call_user(client, message: Message):
    if not is_authorized(message.from_user.id):
        logger.warning(f"Unauthorized call attempt by user {message.from_user.id} at {datetime.now()}")
        await message.reply("You are not authorized to initiate a call!")
        return

    if not check_rate_limit(message.from_user.id):
        logger.info(f"Rate limit exceeded for user {message.from_user.id} at {datetime.now()}")
        await message.reply("You are using commands too frequently. Please try again later.")
        return

    try:
        logger.info(f"User {message.from_user.id} is attempting to join a call at {datetime.now()}")
        
        await tg_calls.join_group_call(message.chat.id, "your_audio_file.mp3")
        logger.info(f"User {message.from_user.id} successfully joined the group call at {datetime.now()}")
        await message.reply("Successfully joined the group call!")
    except Exception as e:
        logger.error(f"Error occurred for user {message.from_user.id} while joining the call: {e}")
        await message.reply("Failed to join the call. Please try again later.")
        
# Enhanced error handling for bot runtime
if __name__ == "__main__":
    try:
        bot.run()
    except Exception as e:
        logger.critical(f"Critical error encountered while running the bot: {e}")
