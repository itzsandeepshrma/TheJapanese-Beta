import logging
from pytgcalls.types import Update
from Telegram.pytgcalls.calls import call_client

LOGGER = logging.getLogger(__name__)

@call_client.on_update()
async def on_call_update(update: Update):
    """Handle voice call updates."""
    LOGGER.info(f"📞 Voice Call Update: {update}")
