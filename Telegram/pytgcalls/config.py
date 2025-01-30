import os

class Config:
    API_ID = os.getenv("API_ID", "your_api_id")
    API_HASH = os.getenv("API_HASH", "your_api_hash")
    BOT_TOKEN = os.getenv("BOT_TOKEN", "your_bot_token")
    DATABASE_FILE = "call_data.json"
    CHAT_ID = 123456789  # Replace with your chat ID
    AUTHORIZED_USERS = [123456789, 987654321]  # Replace with your authorized user IDs
    ENCRYPTION_KEY = os.getenv("ENCRYPTION_KEY", "your_encryption_key")
    REQUEST_LIMIT = 3  # Max requests per user
    REQUEST_TIME_WINDOW = 10  # Time window for rate limiting in seconds
