from pyrogram import Client, filters
from PIL import Image, ImageFilter
import tempfile

@Client.on_message(filters.command("blur"))
async def blur_image(client, message):
    if not message.reply_to_message or not message.reply_to_message.photo:
        await message.reply("Reply to an image to apply blur effect!")
        return

    photo = await message.reply_to_message.download()
    img = Image.open(photo)
    blurred = img.filter(ImageFilter.BLUR)

    temp_file = tempfile.mktemp(suffix=".png")
    blurred.save(temp_file)

    await message.reply_photo(temp_file)
