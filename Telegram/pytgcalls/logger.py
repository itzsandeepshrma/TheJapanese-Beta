import logging
import logging.handlers

class AdvancedLogger:
    def __init__(self, log_file: str):
        self.logger = logging.getLogger("BotLogger")
        handler = logging.handlers.RotatingFileHandler(log_file, maxBytes=5*1024*1024, backupCount=5)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
        self.logger.setLevel(logging.DEBUG)

    def log_info(self, message: str):
        self.logger.info(message)

    def log_error(self, message: str):
        self.logger.error(message)
