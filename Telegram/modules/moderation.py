from pyrogram import Client, filters
from pyrogram.types import Message
import json
import os

BANNED_USERS_FILE = "data/banned_users.json"

# Ensure banned users file exists
if not os.path.exists(BANNED_USERS_FILE):
    with open(BANNED_USERS_FILE, "w") as f:
        json.dump([], f)

@Client.on_message(filters.command("ban") & filters.user("admin_id"))
async def ban_user(client, message: Message):
    try:
        user_id = message.reply_to_message.from_user.id
        with open(BANNED_USERS_FILE, "r+") as f:
            banned_users = json.load(f)
            if user_id not in banned_users:
                banned_users.append(user_id)
                f.seek(0)
                json.dump(banned_users, f)
                await message.reply("User banned successfully.")
    except Exception as e:
        await message.reply(f"Error: {e}")

@Client.on_message(filters.command("unban") & filters.user("admin_id"))
async def unban_user(client, message: Message):
    try:
        user_id = message.reply_to_message.from_user.id
        with open(BANNED_USERS_FILE, "r+") as f:
            banned_users = json.load(f)
            if user_id in banned_users:
                banned_users.remove(user_id)
                f.seek(0)
                f.truncate()
                json.dump(banned_users, f)
                await message.reply("User unbanned successfully.")
    except Exception as e:
        await message.reply(f"Error: {e}")
