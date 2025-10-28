import datetime
import wikipedia
import pywhatkit

def handle_basic(comando: str) -> str:
    t = (comando or "").lower().strip()

    if "horas" in t or "hora" in t:
        hora = datetime.datetime.now().strftime("%H:%M")
        return f"Senhor Guilherme, a hora atual é {hora}."

    if "abrir youtube" in t:
        pywhatkit.playonyt("youtube")
        return "Abrindo YouTube, senhor Guilherme."

    if "pesquisar" in t:
        termo = t.replace("pesquisar", "").strip()
        if not termo:
            return "O que deseja pesquisar?"
        pywhatkit.search(termo)
        return f"Pesquisando {termo} na internet."

    if "quem é" in t:
        pessoa = t.split("quem é", 1)[-1].strip()
        if not pessoa:
            return "Quem você quer saber quem é?"
        try:
            wikipedia.set_lang("pt")
            info = wikipedia.summary(pessoa, sentences=1)
            return info
        except Exception:
            return f"Não encontrei informações confiáveis sobre {pessoa}."

    if "o que é" in t:
        termo = t.split("o que é", 1)[-1].strip()
        if not termo:
            return "O que você quer saber o que é?"
        try:
            wikipedia.set_lang("pt")
            info = wikipedia.summary(termo, sentences=1)
            return info
        except Exception:
            return f"Não encontrei informações confiáveis sobre {termo}."

    if "tocar" in t:
        musica = t.split("tocar", 1)[-1].strip()
        if not musica:
            return "Qual música deseja tocar?"
        pywhatkit.playonyt(musica)
        return f"Tocando {musica} no YouTube."

    if "tchau" in t or "sair" in t or "encerrar" in t:
        return "__EXIT__"

    return "Não entendi. Poderia repetir?"
