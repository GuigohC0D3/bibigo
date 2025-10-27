import speech_recognition as sr
from config.settings import LANG

def ouvir_comando():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Estou te ouvindo...")
        r.pause_threshold = 1
        audio = r.listen(source)
    try:
        print("Reconhecendo...")
        comando = r.recognize_google(audio, language=LANG)
        print(f"Você disse: {comando}\n")
    except sr.UnknownValueError:
        print("Não entendi. Pode repetir?")
        return "nenhum"
    except sr.RequestError as e:
        print(f"Erro ao solicitar resultados do Google Speech Recognition: {e}")
        return "nenhum"
    return comando.lower().strip()
