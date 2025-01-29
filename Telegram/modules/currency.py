from pyrogram import Client, filters
import requests

CURRENCY_API = "https://api.exchangerate-api.com/v4/latest/"

@Client.on_message(filters.command("convert"))
async def convert_currency(client, message):
    try:
        params = message.text.split(" ", 3)
        amount = float(params[1])
        from_currency = params[2].upper()
        to_currency = params[3].upper()

        response = requests.get(f"{CURRENCY_API}{from_currency}").json()
        rate = response["rates"].get(to_currency)

        if not rate:
            await message.reply("Invalid currency code.")
            return

        converted_amount = amount * rate
        await message.reply(f"{amount} {from_currency} = {converted_amount:.2f} {to_currency}")
    except (IndexError, ValueError):
        await message.reply("Usage: .convert <amount> <from_currency> <to_currency>")
    except Exception as e:
        await message.reply(f"Error: {str(e)}")
