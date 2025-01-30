import requests
from pyrogram import Client, filters

API_URL = "https://api.exchangerate-api.com/v4/latest/USD"  # Exchange API

@Client.on_message(filters.command("rate"))
async def get_currency_rate(client, message):
    try:
        response = requests.get(API_URL).json()
        rates = response["rates"]
        message_text = "Current Exchange Rates:\n"
        
        for currency, rate in rates.items():
            message_text += f"{currency}: {rate}\n"

        await message.reply(message_text)
    except Exception as e:
        await message.reply(f"Error: {str(e)}")
