import requests
from pyrogram import Client, filters

JOKE_API = "https://official-joke-api.appspot.com/random_joke"  # Joke API

@Client.on_message(filters.command("joke"))
async def get_joke(client, message):
    try:
        response = requests.get(JOKE_API).json()
        joke = f"{response['setup']}\n{response['punchline']}"
        await message.reply(joke)
    except Exception as e:
        await message.reply(f"Error: {str(e)}")