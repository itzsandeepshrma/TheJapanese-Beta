import os
from dotenv import load_dotenv
from pyrogram import Client
from pyrogram.errors import FloodWait
import logging

# Load environment variables
load_dotenv()

# Fetch configuration variables from .env file
API_ID = os.getenv("API_ID")
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")
STRING_SESSION = os.getenv("STRING_SESSION")
ENABLE_LOGGING = os.getenv("ENABLE_LOGGING", "True") == "True"
LOG_LEVEL = os.getenv("LOG_LEVEL", "DEBUG")

# Configure logging
logging.basicConfig(level=LOG_LEVEL.upper())
logger = logging.getLogger(__name__)

# Initialize the bot client
if STRING_SESSION:
    client = Client("bot_session", api_id=API_ID, api_hash=API_HASH, string_session=STRING_SESSION)
else:
    client = Client("bot_session", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# Log the bot startup
def start_bot():
    try:
        client.start()
        logger.info(f"Bot started as {client.get_me().username}")
    except Exception as e:
        logger.error(f"Error starting bot: {e}")

# Stop the bot gracefully
def stop_bot():
    client.stop()
    logger.info("Bot stopped.")

# Start the bot
if __name__ == "__main__":
    start_bot()
