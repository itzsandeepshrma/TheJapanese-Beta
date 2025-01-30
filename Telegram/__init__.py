import os
import logging
from dotenv import load_dotenv
from pyrogram import Client
from pyrogram.errors import FloodWait
import sys

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

# Check if all required environment variables are present
missing_vars = [var for var in ["API_ID", "API_HASH", "BOT_TOKEN"] if not os.getenv(var)]
if missing_vars:
    for var in missing_vars:
        logger.error(f"Missing environment variable: {var}")
    sys.exit(1)

# Initialize the bot client
try:
    if STRING_SESSION:
        client = Client("bot_session", api_id=API_ID, api_hash=API_HASH, string_session=STRING_SESSION)
        logger.info("Bot client initialized with STRING_SESSION.")
    else:
        client = Client("bot_session", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)
        logger.info("Bot client initialized with BOT_TOKEN.")
except Exception as e:
    logger.error(f"Error initializing bot client: {e}")
    sys.exit(1)

# Log the bot startup
def start_bot():
    try:
        client.start()
        logger.info(f"Bot started as {client.get_me().username}")
    except Exception as e:
        logger.error(f"Error starting bot: {e}")
        sys.exit(1)

# Stop the bot gracefully
def stop_bot():
    try:
        client.stop()
        logger.info("Bot stopped.")
    except Exception as e:
        logger.error(f"Error stopping bot: {e}")

# Start the bot
if __name__ == "__main__":
    try:
        logger.info("Starting bot...")
        start_bot()
    except KeyboardInterrupt:
        stop_bot()
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")
        stop_bot()
