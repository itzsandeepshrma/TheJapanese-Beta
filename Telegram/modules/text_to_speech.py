from gtts import gTTS
from pyrogram import Client, filters
import tempfile

@Client.on_message(filters.command("tts"))
async def text_to_speech(client, message):
    try:
        text = message.text.split(" ", 1)[1]
        temp_file = tempfile.mktemp(suffix=".mp3")
        tts = gTTS(text)
        tts.save(temp_file)

        await message.reply_audio(temp_file)
    except IndexError:
        await message.reply("Please provide text to convert to speech!")
    except Exception as e:
        await message.reply(f"Error: {str(e)}")
