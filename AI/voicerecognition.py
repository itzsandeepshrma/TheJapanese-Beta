import speech_recognition as sr

class VoiceRecognition:
    def __init__(self):
        self.recognizer = sr.Recognizer()

    def listen(self):
        with sr.Microphone() as source:
            print("Listening...")
            audio = self.recognizer.listen(source)
        try:
            print("Recognizing...")
            return self.recognizer.recognize_google(audio)
        except sr.UnknownValueError:
            print("Sorry, I didn't catch that.")
            return None
        except sr.RequestError:
            print("Network error, please try again later.")
            return None

vr = VoiceRecognition()
print(vr.listen())
