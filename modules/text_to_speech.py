import pyttsx3

class TextToSpeech:
    def __init__(self, rate=150, voice_id=None):
        self.engine = pyttsx3.init()
        self.engine.setProperty("rate", rate)
        if voice_id:
            self.engine.setProperty("voice", voice_id)

    def speak_text(self, text):
        self.engine.say(text)
        self.engine.runAndWait()
