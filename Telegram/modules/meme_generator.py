from pyrogram import Client, filters
from PIL import Image, ImageDraw, ImageFont
import tempfile

@Client.on_message(filters.command("meme"))
async def create_meme(client, message):
    try:
        text = message.text.split("\n")
        top_text = text[1].upper()
        bottom_text = text[2].upper()

        temp_file = tempfile.mktemp(suffix=".jpg")
        image = Image.open("template.jpg")  # Add your meme template image in the project
        draw = ImageDraw.Draw(image)
        font = ImageFont.truetype("arial.ttf", 40)

        draw.text((10, 10), top_text, font=font, fill="white")
        draw.text((10, image.height - 50), bottom_text, font=font, fill="white")

        image.save(temp_file)
        await message.reply_photo(temp_file, caption="Here is your meme!")
    except Exception as e:
        await message.reply(f"Error: {str(e)}")
