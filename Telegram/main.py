
import logging
from pyrogram import Client, filters
from pyrogram.types import Message
from . import start_bot, stop_bot  # Importing start/stop functions from __init__.py

# Custom commands or handlers
async def greet_user(client: Client, message: Message):
    await message.reply("Hello, welcome to The-Japanese Bot! How can I assist you today?")

async def echo(client: Client, message: Message):
    await message.reply(message.text)  # Echo the user's message

# Bot command handlers
@client.on_message(filters.command("start"))
async def handle_start(client: Client, message: Message):
    await greet_user(client, message)

@client.on_message(filters.text)
async def handle_text(client: Client, message: Message):
    await echo(client, message)

# Start the bot and handle events
if __name__ == "__main__":
    try:
        start_bot()
    except KeyboardInterrupt:
        stop_bot()
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        stop_bot()
