from pyrogram import Client, filters
from pyrogram.types import Message
from pytgcalls import Client as TgCallsClient
from config import Config
from logger import AdvancedLogger
from session_manager import UserManager
from rate_limiter import RateLimiter
from database import Database
from encryption import ConfigEncryption

# Main Bot Functionality
class Bot:
    def __init__(self):
        self.config = Config()
        self.logger = AdvancedLogger("bot.log")
        self.config_encryption = ConfigEncryption(self.config.ENCRYPTION_KEY)
        self.user_manager = UserManager(self.config.AUTHORIZED_USERS)
        self.rate_limiter = RateLimiter(self.config.REQUEST_LIMIT, self.config.REQUEST_TIME_WINDOW)
        self.db = Database(self.config.DATABASE_FILE)
        self.bot = Client("EnhancedBot", api_id=self.config.API_ID, api_hash=self.config.API_HASH, bot_token=self.config.BOT_TOKEN)

    def validate_input(self, user_id: int, command: str):
        """Validate input commands"""
        if not self.user_manager.is_authorized(user_id):
            self.logger.log_error(f"Unauthorized access attempt by user {user_id}")
            return False, "You are not authorized to perform this action!"
        
        if self.rate_limiter.is_rate_limited(user_id):
            self.logger.log_error(f"Rate limit exceeded by user {user_id}")
            return False, "You are being rate-limited. Try again later."

        return True, ""

    def execute_command(self, user_id: int, command: str):
        """Execute the requested command after validation"""
        valid, message = self.validate_input(user_id, command)
        if not valid:
            return message

        if command == "/start":
            return self.start_command(user_id)
        elif command == "/call":
            return self.call_user_command(user_id)
        elif command == "/end_call":
            return self.end_call_command(user_id)
        else:
            return "Unknown command."

    def start_command(self, user_id: int):
        """Start a command to initiate a bot session"""
        self.user_manager.start_session(user_id)
        self.logger.log_info(f"User {user_id} started a session")
        return "Bot session started. How can I assist you today?"

    def call_user_command(self, user_id: int):
        """Command to initiate a call"""
        self.logger.log_info(f"User {user_id} initiated a call")
        tg_calls = TgCallsClient("call_session")
        try:
            tg_calls.join_group_call(self.config.CHAT_ID, "audio.mp3")
            return "Successfully joined the group call!"
        except Exception as e:
            self.logger.log_error(f"Error while joining the call: {str(e)}")
            return "Failed to join the call. Please try again later."

    def end_call_command(self, user_id: int):
        """End the call and log the duration"""
        call_duration = time.time() - self.user_manager.session_data.get(user_id, 0)
        self.db.add_call_log(user_id, call_duration)
        self.user_manager.end_session(user_id)
        self.logger.log_info(f"User {user_id} ended the call after {call_duration} seconds.")
        return f"Call ended. Duration: {call_duration} seconds."

    def run(self):
        """Run the bot and start listening for commands"""
        self.bot.add_handler(filters.command("start"), self.handle_start)
        self.bot.add_handler(filters.command("call"), self.handle_call)
        self.bot.add_handler(filters.command("end_call"), self.handle_end_call)
        self.bot.run()

    async def handle_start(self, client, message: Message):
        response = self.execute_command(message.from_user.id, "/start")
        await message.reply(response)

    async def handle_call(self, client, message: Message):
        response = self.execute_command(message.from_user.id, "/call")
        await message.reply(response)

    async def handle_end_call(self, client, message: Message):
        response = self.execute_command(message.from_user.id, "/end_call")
        await message.reply(response)

# Initialize and run the bot
if __name__ == "__main__":
    bot = Bot()
    bot.run()
