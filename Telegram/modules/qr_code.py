import qrcode
from pyrogram import Client, filters
import tempfile

@Client.on_message(filters.command("qrcode"))
async def generate_qr(client, message):
    try:
        text = message.text.split(" ", 1)[1]
        temp_file = tempfile.mktemp(suffix=".png")
        img = qrcode.make(text)
        img.save(temp_file)
        await message.reply_photo(temp_file)
    except IndexError:
        await message.reply("Please provide text or URL to generate a QR code!")
