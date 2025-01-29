from pyrogram import Client, filters
import requests

SHORTENER_API = "https://api.shrtco.de/v2/shorten?url="

@Client.on_message(filters.command("shorten"))
async def shorten_url(client, message):
    try:
        url = message.text.split(" ", 1)[1]
        response = requests.get(SHORTENER_API + url).json()

        if response["ok"]:
            short_url = response["result"]["short_link"]
            await message.reply(f"Shortened URL: {short_url}")
        else:
            await message.reply("Failed to shorten the URL. Please try again.")
    except IndexError:
        await message.reply("Usage: .shorten <URL>")
    except Exception as e:
        await message.reply(f"Error: {str(e)}")
