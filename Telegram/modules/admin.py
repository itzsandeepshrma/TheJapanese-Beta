from pyrogram import Client, filters
from pyrogram.types import Message

@Client.on_message(filters.command("mute") & filters.user("admin_id"))
async def mute_user(client, message: Message):
    try:
        user_id = message.reply_to_message.from_user.id
        await client.restrict_chat_member(message.chat.id, user_id, permissions={})
        await message.reply("User muted successfully.")
    except Exception as e:
        await message.reply(f"Error: {e}")

@Client.on_message(filters.command("unmute") & filters.user("admin_id"))
async def unmute_user(client, message: Message):
    try:
        user_id = message.reply_to_message.from_user.id
        await client.unrestrict_chat_member(message.chat.id, user_id)
        await message.reply("User unmuted successfully.")
    except Exception as e:
        await message.reply(f"Error: {e}")
