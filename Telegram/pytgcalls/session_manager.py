import time

class UserManager:
    def __init__(self, authorized_users: list):
        self.authorized_users = set(authorized_users)
        self.session_data = {}

    def is_authorized(self, user_id: int) -> bool:
        """Check if user is authorized"""
        return user_id in self.authorized_users

    def start_session(self, user_id: int):
        """Start a session for an authorized user"""
        if self.is_authorized(user_id):
            self.session_data[user_id] = time.time()
            return True
        return False

    def end_session(self, user_id: int):
        """End a user's session"""
        if user_id in self.session_data:
            del self.session_data[user_id]
            return True
        return False
