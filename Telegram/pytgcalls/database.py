import json
import os

class Database:
    def __init__(self, db_file: str):
        self.db_file = db_file
        self.db = self.load_db()

    def load_db(self) -> dict:
        """Simulate loading data from a database file"""
        if not os.path.exists(self.db_file):
            return {}
        with open(self.db_file, "r") as f:
            return json.load(f)

    def save_db(self):
        """Simulate saving data to the database file"""
        with open(self.db_file, "w") as f:
            json.dump(self.db, f)

    def add_call_log(self, user_id: int, call_duration: float):
        """Simulate saving a call log"""
        self.db.setdefault(str(user_id), []).append(call_duration)
        self.save_db()
