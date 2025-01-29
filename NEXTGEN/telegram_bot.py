import logging
import os
from pyrogram import Client, filters
from pyrogram.types import Message
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from a .env file

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

API_ID = os.getenv("TELEGRAM_API_ID")
API_HASH = os.getenv("TELEGRAM_API_HASH")
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# Initialize the Telegram Bot
app = Client("telegram_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# Commands Handlers
@app.on_message(filters.command("start"))
async def handle_start(client: Client, message: Message):
    try:
        await message.reply("Welcome to The Japanese Bot! How can I assist you today?")
    except Exception as e:
        logger.error(f"Error in /start command: {e}")

@app.on_message(filters.text)
async def echo(client: Client, message: Message):
    try:
        await message.reply(message.text)
    except Exception as e:
        logger.error(f"Error in echoing message: {e}")

# Background Scheduler Example
scheduler = AsyncIOScheduler()

@scheduler.scheduled_job('interval', seconds=60)
def scheduled_task():
    logger.info("Scheduled task running...")

if __name__ == "__main__":
    try:
        scheduler.start()
        app.run()
    except Exception as e:
        logger.error(f"Error: {e}")
        app.stop()
