from pyrogram import Client, filters
import asyncio

reminders = {}

@Client.on_message(filters.command("remindme"))
async def set_reminder(client, message):
    try:
        args = message.text.split(" ", 2)
        time_in_seconds = int(args[1])
        reminder_text = args[2]

        await message.reply(f"Reminder set for {time_in_seconds} seconds!")
        await asyncio.sleep(time_in_seconds)

        await message.reply(f"Reminder: {reminder_text}")
    except IndexError:
        await message.reply("Usage: .remindme <time_in_seconds> <reminder_text>")
    except Exception as e:
        await message.reply(f"Error: {str(e)}")
