from pyrogram import Client, filters
import requests
import os

WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")

@Client.on_message(filters.command("weather"))
async def weather(client, message):
    try:
        city = message.text.split(" ", 1)[1]
        response = requests.get(
            f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}&units=metric"
        ).json()

        if response.get("cod") != 200:
            await message.reply("City not found! Please check the name.")
            return

        weather_data = f"""
🌍 **City**: {response['name']}
🌡️ **Temperature**: {response['main']['temp']}°C
☁️ **Condition**: {response['weather'][0]['description'].capitalize()}
💧 **Humidity**: {response['main']['humidity']}%
💨 **Wind Speed**: {response['wind']['speed']} m/s
"""
        await message.reply(weather_data)
    except IndexError:
        await message.reply("Please provide a city name!")
    except Exception as e:
        await message.reply(f"Error: {str(e)}")
