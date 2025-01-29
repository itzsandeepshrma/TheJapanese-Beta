from pyrogram import Client, filters
from yt_dlp import YoutubeDL
import os
import tempfile

@Client.on_message(filters.command("ytdownload"))
async def youtube_download(client, message):
    try:
        url = message.text.split(" ", 1)[1]  # Extract URL
        await message.reply("Downloading... Please wait!")

        ydl_opts = {
            "format": "best",
            "outtmpl": os.path.join(tempfile.gettempdir(), "%(title)s.%(ext)s"),
        }

        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            file_path = ydl.prepare_filename(info)

        await message.reply_document(file_path)
        os.remove(file_path)  # Clean up after sending
    except Exception as e:
        await message.reply(f"Error: {str(e)}")
