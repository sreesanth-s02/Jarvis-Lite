try:
    import pyttsx3
except ModuleNotFoundError:
    pyttsx3 = None

engine = None
if pyttsx3 is not None:
    engine = pyttsx3.init()
    engine.setProperty("rate", 165)

def speak(text: str) -> None:
    print(f"Assistant: {text}")
    if engine is None:
        return
    engine.say(text)
    engine.runAndWait()