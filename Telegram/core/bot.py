
from pyrogram import Client

app = Client(
    "TheJapaneseBot",
    api_id="YOUR_API_ID",
    api_hash="YOUR_API_HASH",
    session_string="YOUR_SESSION_STRING"
)

if __name__ == "__main__":
    print("✅ Telegram Bot is Running...")
    app.run()
