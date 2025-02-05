from pyrogram import Client, filters
from pytgcalls import PyTgCalls
from pytgcalls.types import AudioPiped

app = Client("TheJapaneseBot")
vc = PyTgCalls(app)

@app.on_message(filters.command("play"))
async def play(_, message):
    chat_id = message.chat.id
    audio_url = "https://example.com/song.mp3"
    await vc.join_group_call(chat_id, AudioPiped(audio_url))
    await message.reply("🎵 Playing in Voice Chat!")

app.run()
