from pyrogram import Client, filters
import requests
import os

DICTIONARY_API = "https://api.dictionaryapi.dev/api/v2/entries/en/"

@Client.on_message(filters.command("define"))
async def define_word(client, message):
    try:
        word = message.text.split(" ", 1)[1]
        response = requests.get(f"{DICTIONARY_API}{word}").json()

        if isinstance(response, dict) and "title" in response:
            await message.reply(f"Word not found: {word}")
            return

        meanings = response[0]["meanings"]
        definition = meanings[0]["definitions"][0]["definition"]

        await message.reply(f"**Word**: {word}\n**Definition**: {definition}")
    except IndexError:
        await message.reply("Please provide a word to define.")
    except Exception as e:
        await message.reply(f"Error: {str(e)}")
