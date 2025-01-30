import time

class RateLimiter:
    def __init__(self, limit: int, time_window: int):
        self.limit = limit
        self.time_window = time_window
        self.user_requests = {}

    def is_rate_limited(self, user_id: int) -> bool:
        current_time = time.time()
        if user_id not in self.user_requests:
            self.user_requests[user_id] = []

        requests = self.user_requests[user_id]
        requests = [req_time for req_time in requests if current_time - req_time < self.time_window]
        
        self.user_requests[user_id] = requests

        if len(requests) >= self.limit:
            return True

        self.user_requests[user_id].append(current_time)
        return False
