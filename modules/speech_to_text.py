import speech_recognition as sr

class SpeechToText:
    def __init__(self):
        self.recognizer = sr.Recognizer()

    def record_and_transcribe(self):
        with sr.Microphone() as source:
            self.recognizer.adjust_for_ambient_noise(source, duration=1)  # Improved noise filtering
            try:
                audio = self.recognizer.listen(source, timeout=10, phrase_time_limit=15)
                transcript = self.recognizer.recognize_google(audio)
                return transcript, transcript
            except sr.UnknownValueError:
                return None, "I couldn't understand your response."
            except sr.RequestError as e:
                return None, f"Error with the recognition service: {e}"
