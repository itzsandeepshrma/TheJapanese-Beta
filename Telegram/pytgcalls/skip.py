from pytgcalls import Client as TgCallsClient
from pyrogram import Client, filters
from pyrogram.types import Message

# Initialize your bot and calls client
bot = Client("YourBot", api_id=API_ID, api_hash=API_HASH)
tg_calls = TgCallsClient("call_session")

# Function to skip currently playing audio/video
@bot.on_message(filters.command("skip"))
async def skip_track(client, message: Message):
    # Check if the user is authorized
    if message.from_user.id not in authorized_users:
        await message.reply("You are not authorized to skip the track!")
        return

    # Handle skipping the track
    try:
        # If the bot is already in a call, attempt to skip the audio/video
        if tg_calls.is_call_active(message.chat.id):
            await tg_calls.stop(message.chat.id)  # Stop the current playback
            await tg_calls.play(message.chat.id, "next_audio_file.mp3")  # Play the next file
            await message.reply("Successfully skipped the current track!")
        else:
            await message.reply("No active call to skip the track.")
    except Exception as e:
        await message.reply(f"Error while skipping track: {str(e)}")
