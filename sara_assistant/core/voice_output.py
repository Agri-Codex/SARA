import pyttsx3

class VoiceOutput:
    def __init__(self):
        self.engine = pyttsx3.init()
        self.engine.setProperty("rate", 170)

    def speak(self, text: str):
        print(f"SARA: {text}")
        self.engine.say(text)
        self.engine.runAndWait()
