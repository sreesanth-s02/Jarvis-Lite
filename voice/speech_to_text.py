try:
    import speech_recognition as sr
except ModuleNotFoundError:
    sr = None

class SpeechRecognizer:
    def __init__(self):
        if sr is None:
            self.recognizer = None
            return

        self.recognizer = sr.Recognizer()
        self.recognizer.energy_threshold = 250
        self.recognizer.pause_threshold = 0.8
        self.recognizer.dynamic_energy_threshold = True

    def listen_once(self) -> str:
        if sr is None or self.recognizer is None:
            print("SpeechRecognition is not installed. Voice input is disabled.")
            return ""

        with sr.Microphone() as source:
            print("Listening...")
            self.recognizer.adjust_for_ambient_noise(source, duration=1)

            try:
                audio = self.recognizer.listen(
                    source,
                    timeout=10,
                    phrase_time_limit=7
                )
            except sr.WaitTimeoutError:
                print("No speech detected. Please try again.")
                return ""

        try:
            text = self.recognizer.recognize_google(audio)
            return text.strip().lower()
        except sr.UnknownValueError:
            print("Could not understand")
            return ""
        except sr.RequestError as e:
            print(f"Speech service error: {e}")
            return ""