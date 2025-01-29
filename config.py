import os
import logging
import sys
from dotenv import load_dotenv
from cryptography.fernet import Fernet
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Load environment variables
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

# Telegram bot related env variables
API_ID = os.getenv("API_ID")
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")
STRING_SESSION = os.getenv("STRING_SESSION")
OWNER_ID = os.getenv("OWNER_ID")

# Database configuration (SQLAlchemy)
DB_URI = os.getenv("DB_URI", "sqlite:///db.sqlite3")
DB_NAME = os.getenv("DB_NAME", "bot_db")

# Proxy and deployment configuration
PROXY = os.getenv("PROXY", None)
DEPLOYMENT_MODE = os.getenv("DEPLOYMENT_MODE", "production")
TIMEZONE = os.getenv("TIMEZONE", "Asia/Kolkata")

# Logging configuration
ENABLE_LOGGING = os.getenv("ENABLE_LOGGING", "True") == "True"
LOG_LEVEL = os.getenv("LOG_LEVEL", "DEBUG").upper()

# Configure logging
logging.basicConfig(level=LOG_LEVEL, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger()

def validate_env_vars():
    required_vars = {
        "API_ID": API_ID,
        "API_HASH": API_HASH,
        "BOT_TOKEN": BOT_TOKEN,
        "STRING_SESSION": STRING_SESSION,
        "OWNER_ID": OWNER_ID
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
    
    logger.info("\n🗄️ Database Configuration 🗄️")
    logger.info(f"DB_URI: {DB_URI}")
    logger.info(f"DB_NAME: {DB_NAME}")

    logger.info("\n⚙️ Other Settings ⚙️")
    logger.info(f"PROXY: {PROXY}")
    logger.info(f"DEPLOYMENT_MODE: {DEPLOYMENT_MODE}")
    logger.info(f"TIMEZONE: {TIMEZONE}")
    logger.info(f"ENABLE_LOGGING: {ENABLE_LOGGING}")
    logger.info(f"LOG_LEVEL: {LOG_LEVEL}")

# Encrypt sensitive data like owner ID if needed
encrypted_owner_id = encrypt_sensitive_data(OWNER_ID, ENCRYPTION_KEY)
logger.info(f"Encrypted Owner ID: {encrypted_owner_id}")

# Decrypt sensitive data like owner ID if needed
decrypted_owner_id = decrypt_sensitive_data(encrypted_owner_id, ENCRYPTION_KEY)
logger.info(f"Decrypted Owner ID: {decrypted_owner_id}")

# Set up SQLAlchemy for database connection
engine = create_engine(DB_URI)
Session = sessionmaker(bind=engine)
session = Session()

# Example: Define a simple table
from sqlalchemy import Column, Integer, String

class User(session):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    password = Column(String)

# Create tables if not exist
Base.metadata.create_all(engine)

if __name__ == "__main__":
    try:
        validate_env_vars()
        print_config()
    except ValueError as e:
        logger.error(f"Error: {e}")
        sys.exit(1)
