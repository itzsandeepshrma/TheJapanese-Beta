import time

BLACKLIST = {}

def rate_limit(user_id):
    if user_id in BLACKLIST and time.time() - BLACKLIST[user_id] < 10:
        return True
    BLACKLIST[user_id] = time.time()
    return False
