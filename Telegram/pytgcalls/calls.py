from pytgcalls import PyTgCalls
from pyrogram import Client
from config import API_ID, API_HASH, SESSION_STRING
import logging

logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(__name__)

app = Client("Userbot", api_id=API_ID, api_hash=API_HASH, session_string=SESSION_STRING1)

call_client = PyTgCalls(app)

async def start_pytgcalls():
    """Start PyTgCalls service."""
    try:
        await call_client.start()
        LOGGER.info("✅ PyTgCalls started successfully.")
    except Exception as e:
        LOGGER.error(f"⚠️ PyTgCalls Error: {e}")

async def stop_pytgcalls():
    """Stop PyTgCalls service."""
    await call_client.stop()
    LOGGER.info("❌ PyTgCalls stopped.")
