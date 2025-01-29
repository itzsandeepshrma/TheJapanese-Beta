import os
from dotenv import load_dotenv
from cryptography.fernet import Fernet
import logging
import sys

load_dotenv()

def generate_key():
    return Fernet.generate_key()

def encrypt_sensitive_data(data: str, key: bytes):
    cipher = Fernet(key)
    encrypted_data = cipher.encrypt(data.encode())
    return encrypted_data

def decrypt_sensitive_data(encrypted_data: bytes, key: bytes):
    cipher = Fernet(key)
    decrypted_data = cipher.decrypt(encrypted_data).decode()
    return decrypted_data

ENCRYPTION_KEY = os.getenv("ENCRYPTION_KEY", generate_key().decode())

API_ID = os.getenv("API_ID")
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")
STRING_SESSION = os.getenv("STRING_SESSION")
OWNER_ID = os.getenv("OWNER_ID")

WA_API_ID = os.getenv("WA_API_ID")
WA_API_HASH = os.getenv("WA_API_HASH")
WA_BOT_TOKEN = os.getenv("WA_BOT_TOKEN")

INSTAGRAM_USERNAME = os.getenv("INSTAGRAM_USERNAME")
INSTAGRAM_PASSWORD = os.getenv("INSTAGRAM_PASSWORD")
INSTAGRAM_API_KEY = os.getenv("INSTAGRAM_API_KEY")

DB_URI = os.getenv("DB_URI", "sqlite:///db.sqlite3")
DB_NAME = os.getenv("DB_NAME", "bot_db")

PROXY = os.getenv("PROXY", None)
DEPLOYMENT_MODE = os.getenv("DEPLOYMENT_MODE", "production")
TIMEZONE = os.getenv("TIMEZONE", "Asia/Kolkata")

TELEGRAM_GROUP_ID = os.getenv("TELEGRAM_GROUP_ID")
TELEGRAM_CHANNEL_ID = os.getenv("TELEGRAM_CHANNEL_ID")

ENABLE_LOGGING = os.getenv("ENABLE_LOGGING", "True") == "True"
LOG_LEVEL = os.getenv("LOG_LEVEL", "DEBUG").upper()
ENABLE_AUTO_UPDATES = os.getenv("ENABLE_AUTO_UPDATES", "True") == "True"
ENABLE_SESSION_SAVE = os.getenv("ENABLE_SESSION_SAVE", "True") == "True"

logging.basicConfig(level=LOG_LEVEL, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger()

def validate_env_vars():
    required_vars = {
        "API_ID": API_ID,
        "API_HASH": API_HASH,
        "BOT_TOKEN": BOT_TOKEN,
        "STRING_SESSION": STRING_SESSION,
        "OWNER_ID": OWNER_ID,
        "WA_API_ID": WA_API_ID,
        "WA_API_HASH": WA_API_HASH,
        "WA_BOT_TOKEN": WA_BOT_TOKEN,
        "INSTAGRAM_USERNAME": INSTAGRAM_USERNAME,
        "INSTAGRAM_PASSWORD": INSTAGRAM_PASSWORD,
        "INSTAGRAM_API_KEY": INSTAGRAM_API_KEY
    }

    for var, value in required_vars.items():
        if not value:
            logger.error(f"Environment variable {var} is missing!")
            raise ValueError(f"Missing environment variable: {var}")

def print_config():
    logger.info("🌟 Bot Configuration 🌟")
    logger.info(f"API_ID: {API_ID}")
    logger.info(f"API_HASH: {API_HASH}")
    logger.info(f"BOT_TOKEN: {BOT_TOKEN}")
    logger.info(f"STRING_SESSION: {STRING_SESSION}")
    logger.info(f"OWNER_ID: {OWNER_ID}")
    
    logger.info("\n📱 WhatsApp Configuration 📱")
    logger.info(f"WA_API_ID: {WA_API_ID}")
    logger.info(f"WA_API_HASH: {WA_API_HASH}")
    logger.info(f"WA_BOT_TOKEN: {WA_BOT_TOKEN}")
    
    logger.info("\n📸 Instagram Configuration 📸")
    logger.info(f"INSTAGRAM_USERNAME: {INSTAGRAM_USERNAME}")
    logger.info(f"INSTAGRAM_API_KEY: {INSTAGRAM_API_KEY}")
    
    logger.info("\n🗄️ Database Configuration 🗄️")
    logger.info(f"DB_URI: {DB_URI}")
    logger.info(f"DB_NAME: {DB_NAME}")

    logger.info("\n⚙️ Other Settings ⚙️")
    logger.info(f"PROXY: {PROXY}")
    logger.info(f"DEPLOYMENT_MODE: {DEPLOYMENT_MODE}")
    logger.info(f"TIMEZONE: {TIMEZONE}")
    logger.info(f"ENABLE_LOGGING: {ENABLE_LOGGING}")
    logger.info(f"LOG_LEVEL: {LOG_LEVEL}")
    logger.info(f"ENABLE_AUTO_UPDATES: {ENABLE_AUTO_UPDATES}")
    logger.info(f"ENABLE_SESSION_SAVE: {ENABLE_SESSION_SAVE}")

encrypted_instagram_password = encrypt_sensitive_data(INSTAGRAM_PASSWORD, ENCRYPTION_KEY)
logger.info(f"Encrypted Instagram password: {encrypted_instagram_password}")

decrypted_instagram_password = decrypt_sensitive_data(encrypted_instagram_password, ENCRYPTION_KEY)
logger.info(f"Decrypted Instagram password: {decrypted_instagram_password}")

if __name__ == "__main__":
    try:
        validate_env_vars()
        print_config()
    except ValueError as e:
        logger.error(f"Error: {e}")
        sys.exit(1)
