from pytgcalls import Client as TgCallsClient
from pyrogram import Client, filters
from pyrogram.types import Message

# Initialize your bot and calls client
bot = Client("YourBot", api_id=API_ID, api_hash=API_HASH)
tg_calls = TgCallsClient("call_session")

# Function to pause currently playing audio/video
@bot.on_message(filters.command("pause"))
async def pause_track(client, message: Message):
    # Check if the user is authorized
    if message.from_user.id not in authorized_users:
        await message.reply("You are not authorized to pause the track!")
        return

    # Handle pausing the track
    try:
        # If the bot is in a call, attempt to pause the audio/video
        if tg_calls.is_call_active(message.chat.id):
            await tg_calls.pause(message.chat.id)  # Pause the current playback
            await message.reply("Track has been paused.")
        else:
            await message.reply("No active call to pause the track.")
    except Exception as e:
        await message.reply(f"Error while pausing track: {str(e)}")
