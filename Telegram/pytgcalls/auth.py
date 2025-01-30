import hashlib
import time

class AuthManager:
    def __init__(self):
        self.user_tokens = {}

    def generate_token(self, user_id: int) -> str:
        token = f"{user_id}{time.time()}"
        hashed_token = hashlib.sha256(token.encode()).hexdigest()
        self.user_tokens[user_id] = hashed_token
        return hashed_token

    def validate_token(self, user_id: int, token: str) -> bool:
        return self.user_tokens.get(user_id) == token
