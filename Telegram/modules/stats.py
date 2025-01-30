from pyrogram import Client, filters

user_data = {}  # Dictionary to track user stats (expandable to database)

@Client.on_message(filters.command("stats"))
async def get_user_stats(client, message):
    user_id = message.from_user.id
    if user_id in user_data:
        stats = user_data[user_id]
        await message.reply(f"Your stats:\nMessages sent: {stats['messages_sent']}")
    else:
        await message.reply("You haven't interacted much yet. Start chatting!")

@Client.on_message(filters.text)
async def track_user_activity(client, message):
    user_id = message.from_user.id
    if user_id not in user_data:
        user_data[user_id] = {"messages_sent": 0}
    
    user_data[user_id]["messages_sent"] += 1