from pyrogram import Client, filters

@Client.on_message(filters.command("calc"))
async def calculator(client, message):
    try:
        expression = message.text.split(" ", 1)[1]
        result = eval(expression)
        await message.reply(f"Result: {result}")
    except IndexError:
        await message.reply("Usage: .calc <expression>")
    except Exception as e:
        await message.reply(f"Error: {str(e)}")
