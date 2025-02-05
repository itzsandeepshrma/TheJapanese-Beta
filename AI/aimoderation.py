import re

class AIModeration:
    def __init__(self):
        self.banned_words = ["spam", "scam", "hate", "violence"]

    def check_message(self, message):
        for word in self.banned_words:
            if re.search(r'\b' + re.escape(word) + r'\b', message.lower()):
                return False
        return True

moderator = AIModeration()
message = "This is a harmless message"
if moderator.check_message(message):
    print("Message is safe.")
else:
    print("Message contains banned content.")
