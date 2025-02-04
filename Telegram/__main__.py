import asyncio
import logging
import signal
from pyrogram import Client
from config import API_ID, API_HASH, SESSION_STRING
from Telegram.pytgcalls.calls import start_pytgcalls, stop_pytgcalls
import Telegram.pytgcalls.handlers  

logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(__name__)

app = Client("Userbot", api_id=API_ID, api_hash=API_HASH, session_string=SESSION_STRING1)

async def start_services():
    """Start both Userbot and PyTgCalls with proper signal handling."""
    try:
        await app.start()
        LOGGER.info("🚀 Userbot started successfully.")

        await start_pytgcalls()
        LOGGER.info("🎵 Voice Call Client started successfully.")

        LOGGER.info("🔥 The Japanese Userbot is now running!")

        await asyncio.Event().wait()

    except Exception as e:
        LOGGER.error(f"⚠️ Error starting services: {e}")

    finally:
        await shutdown_services()

async def shutdown_services():
    """Gracefully stop all services."""
    LOGGER.info("⚠️ Stopping services...")
    await stop_pytgcalls()
    await app.stop()
    LOGGER.info("✅ Services stopped successfully.")

def signal_handler(sig, frame):
    asyncio.create_task(shutdown_services())

signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)

if __name__ == "__main__":
    try:
        asyncio.run(start_services())
    except KeyboardInterrupt:
        LOGGER.info("🛑 Manual stop detected. Exiting...")
