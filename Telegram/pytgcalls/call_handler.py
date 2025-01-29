import logging
from pytgcalls import Client as TgCallsClient
from pyrogram import Client, filters
from pyrogram.types import Message

# Setup logging for debugging and error tracking
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger()

# Create bot client
bot = Client("YourBot", api_id=API_ID, api_hash=API_HASH)

# Helper function to verify if the user is authorized
def is_authorized(user_id):
    authorized_users = [123456789, 987654321]  # Add your user IDs here
    return user_id in authorized_users

# Command to start the bot
@bot.on_message(filters.command("start"))
async def start(client, message: Message):
    if not is_authorized(message.from_user.id):
        await message.reply("You are not authorized to use this bot!")
        return
    await message.reply("Bot Started! How can I assist you today?")

# Command to initiate a call
@bot.on_message(filters.command("call"))
async def call_user(client, message: Message):
    if not is_authorized(message.from_user.id):
        await message.reply("You are not authorized to initiate a call!")
        return

    tg_calls = TgCallsClient("call_session")
    
    try:
        await tg_calls.join_group_call(message.chat.id, "your_audio_file.mp3")
        await message.reply("Successfully joined the group call!")
    except Exception as e:
        logger.error(f"Error while joining the call: {e}")
        await message.reply("Failed to join the call. Please try again later.")

# Start the bot
if __name__ == "__main__":
    bot.run()
