import logging
import time
import os
from dotenv import load_dotenv
from pyrogram.types import User
from pytgcalls import Client as TgCallsClient

# Load environment variables securely
load_dotenv()

API_ID = os.getenv('API_ID')
API_HASH = os.getenv('API_HASH')
AUTHORIZED_USERS = list(map(int, os.getenv('AUTHORIZED_USERS').split(',')))
RATE_LIMIT_TIME = 10  # Rate limit in seconds

# Setup detailed logging for debugging and error tracking
logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# Track last command usage time for rate limiting
last_used = {}

# Initialize the group call client
tg_calls = TgCallsClient("call_session")

# Helper function to verify if the user is authorized
def is_authorized(user_id: int) -> bool:
    """
    Checks if a user is authorized to use bot commands.
    """
    if user_id in AUTHORIZED_USERS:
        return True
    logger.warning(f"Unauthorized access attempt by user {user_id}")
    return False

# Helper function to check if the user is rate-limited
def check_rate_limit(user_id: int) -> bool:
    """
    Checks if a user is rate-limited based on the time between their last command execution.
    """
    global last_used
    current_time = time.time()

    if user_id in last_used:
        elapsed_time = current_time - last_used[user_id]
        if elapsed_time < RATE_LIMIT_TIME:  # Rate limit exceeded
            logger.info(f"Rate limit exceeded for user {user_id}. Last action was {elapsed_time:.2f} seconds ago.")
            return False
    last_used[user_id] = current_time
    return True

# Helper function to start a group call
async def start_group_call(chat_id: int, audio_url: str) -> bool:
    """
    Starts a group call and plays audio in the given chat.
    """
    try:
        logger.info(f"Starting group call for chat {chat_id} and playing audio from {audio_url}.")
        await tg_calls.join_group_call(chat_id, audio_url)
        logger.info(f"Successfully started group call for chat {chat_id}.")
        return True
    except Exception as e:
        logger.error(f"Error starting group call for chat {chat_id}: {e}")
        return False

# Helper function to stop a group call
async def stop_group_call(chat_id: int) -> bool:
    """
    Stops the ongoing group call in the given chat.
    """
    try:
        logger.info(f"Stopping group call for chat {chat_id}.")
        await tg_calls.stop_audio(chat_id)
        logger.info(f"Successfully stopped group call for chat {chat_id}.")
        return True
    except Exception as e:
        logger.error(f"Error stopping group call for chat {chat_id}: {e}")
        return False

# Helper function to send a warning message to the user if unauthorized
async def send_warning(user: User, message: str) -> None:
    """
    Sends a warning message to a user if they are unauthorized or rate-limited.
    """
    try:
        logger.info(f"Sending warning to user {user.id}.")
        await user.send_message(message)
    except Exception as e:
        logger.error(f"Failed to send warning to user {user.id}: {e}")

# Helper function to manage the call session
def manage_session(action: str) -> None:
    """
    Manages the session based on the action provided.
    """
    try:
        if action == "start":
            tg_calls.start()
            logger.info("Session started successfully.")
        elif action == "stop":
            tg_calls.stop()
            logger.info("Session stopped successfully.")
        else:
            logger.warning(f"Unknown session action: {action}")
    except Exception as e:
        logger.error(f"Failed to manage session with action '{action}': {e}")

# Function to handle command authorization and rate-limiting before executing an action
async def execute_command(client, message, command_action: str, audio_url: str = None):
    """
    Handles the command execution, checking for authorization and rate-limiting.
    """
    user = message.from_user
    if not is_authorized(user.id):
        await send_warning(user, "You are not authorized to execute this command!")
        return

    if not check_rate_limit(user.id):
        await send_warning(user, "You are using commands too frequently. Please try again later.")
        return

    # Execute action based on the command
    if command_action == "start_call" and audio_url:
        await start_group_call(message.chat.id, audio_url)
    elif command_action == "stop_call":
        await stop_group_call(message.chat.id)
    else:
        logger.warning(f"Unknown command action: {command_action}")
        await send_warning(user, "Invalid command action or missing parameters.")

# Example of how this helper might be used in a bot command handler
async def handle_voice_start(client, message):
    audio_url = message.text.split(" ", 1)[-1].strip()  # Extract audio URL
    await execute_command(client, message, "start_call", audio_url)

async def handle_voice_end(client, message):
    await execute_command(client, message, "stop_call")
