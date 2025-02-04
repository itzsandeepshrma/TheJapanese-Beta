import os
import logging
import sys
import asyncio
from datetime import datetime
from logging.handlers import RotatingFileHandler
from aiohttp import ClientSession
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from gpytranslate import Translator
from pyrogram import Client
from pytgcalls import GroupCallFactory
from dotenv import load_dotenv

load_dotenv()

API_ID = os.getenv("API_ID")
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")
STRING_SESSION1 = os.getenv("STRING_SESSION1")

if not API_ID or not API_HASH or not BOT_TOKEN:
    sys.exit("Error: Missing necessary environment variables.")

logging.basicConfig(
    level=logging.INFO,
    format="[%(levelname)s] - %(name)s - %(message)s",
    datefmt="%d-%b-%y %H:%M:%S",
    handlers=[
        RotatingFileHandler("logs.txt", maxBytes=50000000, backupCount=10),
        logging.StreamHandler(),
    ],
)

LOGS = logging.getLogger(__name__)

trl = Translator()
aiosession = ClientSession()

scheduler = AsyncIOScheduler()
StartTime = time.time()
START_TIME = datetime.now()

clients = []
ids = []

app = Client(
    name="app",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
    plugins=dict(root="Telegram/modules/bot"),
    in_memory=True,
)

def create_bot(session_string: str, name: str):
    return Client(
        name=name,
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=session_string,
        plugins=dict(root="Telegram/modules"),
    ) if session_string else None

bots = [
    create_bot(STRING_SESSION1, "bot1"),
]

bots = [bot for bot in bots if bot]

for bot in bots:
    if not hasattr(bot, "group_call"):
        setattr(bot, "group_call", GroupCallFactory(bot).get_group_call())

async def start_bot():
    try:
        await app.start()
        bot_user = await app.get_me()
        LOGS.info(f"Bot started as @{bot_user.username}")
        await asyncio.gather(*(bot.start() for bot in bots))
        await asyncio.sleep(3600)
    except Exception as e:
        LOGS.error(f"Error starting bot: {e}")
        sys.exit(1)

async def stop_bot():
    try:
        await app.stop()
        await asyncio.gather(*(bot.stop() for bot in bots))
        LOGS.info("Bot stopped.")
    except Exception as e:
        LOGS.error(f"Error stopping bot: {e}")

asyncio.run(start_bot())
