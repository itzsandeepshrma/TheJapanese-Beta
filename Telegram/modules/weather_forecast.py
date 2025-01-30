import requests
from pyrogram import Client, filters

API_KEY = "your_openweathermap_api_key"

@Client.on_message(filters.command("forecast"))
async def get_weather_forecast(client, message):
    try:
        city_name = message.text.split(" ", 1)[1]
        url = f"http://api.openweathermap.org/data/2.5/forecast?q={city_name}&appid={API_KEY}&units=metric"
        response = requests.get(url).json()

        if response["cod"] == "200":
            forecast_text = f"5-day forecast for {city_name}:\n"
            for forecast in response["list"]:
                time = forecast["dt_txt"]
                temp = forecast["main"]["temp"]
                weather = forecast["weather"][0]["description"]
                forecast_text += f"{time}: {temp}°C, {weather}\n"
            
            await message.reply(forecast_text)
        else:
            await message.reply("City not found.")
    except IndexError:
        await message.reply("Usage: .forecast <city_name>")
    except Exception as e:
        await message.reply(f"Error: {str(e)}")