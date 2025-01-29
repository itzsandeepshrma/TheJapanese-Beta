import os
import logging
from pyrogram import Client, filters
from pyrogram.types import Message
from dotenv import load_dotenv
import sys

# Load environment variables
load_dotenv()

# Setup logging for better error tracking and debugging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger()

# Fetch API keys and tokens from environment variables
API_ID = os.getenv("API_ID")
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")

if not all([API_ID, API_HASH, BOT_TOKEN]):
    logger.error("API_ID, API_HASH, or BOT_TOKEN is missing in the environment variables.")
    sys.exit(1)

# Create a Pyrogram Client instance
client = Client("The-Japanese-Bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# Define bot commands and handlers

async def greet_user(client: Client, message: Message):
    await message.reply("Hello, welcome to The-Japanese Bot! How can I assist you today?")

async def echo(client: Client, message: Message):
    await message.reply(message.text)  # Echoes the user's message back

# Command: /start
@client.on_message(filters.command("start"))
async def handle_start(client: Client, message: Message):
    await greet_user(client, message)

# Handle all text messages
@client.on_message(filters.text)
async def handle_text(client: Client, message: Message):
    await echo(client, message)

# Start the bot
if __name__ == "__main__":
    try:
        logger.info("Starting The-Japanese Bot...")
        client.run()  # Runs the bot until it is manually stopped
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        sys.exit(1)
