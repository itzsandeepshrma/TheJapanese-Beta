import random

class Chatbot:
    def __init__(self):
        self.responses = {
            "hello": ["Hi there!", "Hello!", "Greetings!"],
            "how are you": ["I'm doing well, thank you!", "I'm good, how about you?", "Doing great! How can I help?"],
            "bye": ["Goodbye!", "See you later!", "Take care!"],
            "default": ["Sorry, I didn't quite understand that.", "Can you say that again?", "I'm not sure how to respond to that."]
        }

    def get_response(self, user_message):
        user_message = user_message.lower()
        for key in self.responses:
            if key in user_message:
                return random.choice(self.responses[key])
        return random.choice(self.responses["default"])


chatbot = Chatbot()
print(chatbot.get_response("Hello, how are you?"))
