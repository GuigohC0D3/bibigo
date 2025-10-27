import pyttsx3

_engine = None

def _get_engine():
    global _engine
    if _engine is None:
        _engine = pyttsx3.init()
        _engine.setProperty("rate", 180)
    return _engine

def falar(texto: str):
    eng = _get_engine()
    eng.say(texto)
    eng.runAndWait()
