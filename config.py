import os
import logging
import sys
import traceback
from dotenv import load_dotenv
from cryptography.fernet import Fernet
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base

load_dotenv()

def generate_key() -> bytes:
    """Generate a new encryption key."""
    return Fernet.generate_key()

def encrypt_sensitive_data(data: str, key: bytes) -> bytes:
    """Encrypt sensitive data using Fernet encryption."""
    cipher = Fernet(key)
    return cipher.encrypt(data.encode())

def decrypt_sensitive_data(encrypted_data: bytes, key: bytes) -> str:
    """Decrypt sensitive data using Fernet encryption."""
    cipher = Fernet(key)
    return cipher.decrypt(encrypted_data).decode()

ENCRYPTION_KEY = os.getenv("ENCRYPTION_KEY", generate_key().decode())

if len(ENCRYPTION_KEY) != 44:
    raise ValueError("Invalid ENCRYPTION_KEY length. Ensure it is a valid Fernet key.")

def get_env_var(var_name, default=None, required=False):
    """Retrieve an environment variable with optional strict validation."""
    value = os.getenv(var_name, default)
    if required and not value:
        raise EnvironmentError(f"Environment variable {var_name} is missing or empty!")
    return value

API_ID = int(get_env_var("API_ID", required=True))
API_HASH = get_env_var("API_HASH", required=True)
BOT_TOKEN = get_env_var("BOT_TOKEN", required=True)
STRING_SESSION = get_env_var("STRING_SESSION", required=True)
OWNER_ID = get_env_var("OWNER_ID", required=True)

DB_URI = get_env_var("DB_URI", "sqlite:///db.sqlite3")
if not DB_URI.startswith(("sqlite://", "postgresql://", "mysql://")):
    raise ValueError("Invalid DB_URI. Must start with 'sqlite://', 'postgresql://', or 'mysql://'.")

PROXY = get_env_var("PROXY")
DEPLOYMENT_MODE = get_env_var("DEPLOYMENT_MODE", "production").lower()
TIMEZONE = get_env_var("TIMEZONE", "Asia/Kolkata")

ENABLE_LOGGING = get_env_var("ENABLE_LOGGING", "True") == "True"
LOG_LEVEL = get_env_var("LOG_LEVEL", "DEBUG").upper()

logging.basicConfig(level=LOG_LEVEL, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger()

def validate_env_vars():
    """Validate critical environment variables."""
    required_vars = {
        "API_ID": API_ID,
        "API_HASH": API_HASH,
        "BOT_TOKEN": BOT_TOKEN,
        "STRING_SESSION": STRING_SESSION,
        "OWNER_ID": OWNER_ID,
    }

    for var, value in required_vars.items():
        if not value:
            logger.error(f"Environment variable {var} is missing or invalid!")
            raise ValueError(f"Missing or invalid environment variable: {var}")

def print_config():
    """Log configuration details for debugging purposes."""
    logger.info("🌟 Bot Configuration 🌟")
    logger.info(f"API_ID: {API_ID}")
    logger.info(f"API_HASH: {API_HASH}")
    logger.info(f"BOT_TOKEN: [HIDDEN]")
    logger.info(f"STRING_SESSION: [HIDDEN]")
    logger.info(f"OWNER_ID: [HIDDEN]")

    logger.info("\n⚙️ Other Settings ⚙️")
    logger.info(f"DB_URI: {DB_URI}")
    logger.info(f"PROXY: {PROXY}")
    logger.info(f"DEPLOYMENT_MODE: {DEPLOYMENT_MODE}")
    logger.info(f"TIMEZONE: {TIMEZONE}")
    logger.info(f"ENABLE_LOGGING: {ENABLE_LOGGING}")
    logger.info(f"LOG_LEVEL: {LOG_LEVEL}")

try:
    encrypted_owner_id = encrypt_sensitive_data(OWNER_ID, ENCRYPTION_KEY.encode())
    logger.info(f"Encrypted Owner ID: {encrypted_owner_id}")
    
    decrypted_owner_id = decrypt_sensitive_data(encrypted_owner_id, ENCRYPTION_KEY.encode())
    logger.info(f"Decrypted Owner ID: {decrypted_owner_id}")
except Exception as e:
    logger.error(f"Encryption/Decryption Error: {traceback.format_exc()}")

Base = declarative_base()
engine = create_engine(DB_URI, pool_pre_ping=True, echo=False)
Session = sessionmaker(bind=engine)
session = Session()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), unique=True, nullable=False)
    password = Column(String(256), nullable=False)

Base.metadata.create_all(engine)

if __name__ == "__main__":
    try:
        validate_env_vars()
        print_config()
    except ValueError as e:
        logger.error(f"Critical Error: {e}")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Unexpected Error: {traceback.format_exc()}")
        sys.exit(1)
