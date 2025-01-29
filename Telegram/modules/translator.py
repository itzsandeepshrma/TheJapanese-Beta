from googletrans import Translator
from pyrogram import Client, filters

translator = Translator()

@Client.on_message(filters.command("translate"))
async def translate_text(client, message):
    try:
        text, dest_lang = message.text.split(" ", 2)[1:]
        translated = translator.translate(text, dest=dest_lang)

        await message.reply(f"**Translated Text**: {translated.text}")
    except IndexError:
        await message.reply("Usage: .translate <text> <destination_language>")
    except Exception as e:
        await message.reply(f"Error: {str(e)}")
