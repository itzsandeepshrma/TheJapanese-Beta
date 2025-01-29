from pyrogram import Client, filters
from pyrogram.types import Message
import openai
import os

# Load OpenAI API Key
openai.api_key = os.getenv("OPENAI_API_KEY")

@Client.on_message(filters.text & ~filters.command)
async def ai_chat(client, message: Message):
    try:
        # Send user text to OpenAI
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=message.text,
            max_tokens=100,
            n=1,
            stop=None,
            temperature=0.7
        )
        reply = response.choices[0].text.strip()
        await message.reply(reply)
    except Exception as e:
        await message.reply("I'm having trouble responding right now. Please try again later.")
