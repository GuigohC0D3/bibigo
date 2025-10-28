# voice/falar.py (neural online + fallback offline)
import asyncio
import os
import tempfile
import pyttsx3

# ---- TTS Neural (Edge) ----
try:
    import edge_tts  # pip install edge-tts
    EDGE_OK = True
except Exception:
    EDGE_OK = False

# ---- Offline fallback ----
_engine = None
def _get_engine():
    global _engine
    if _engine is None:
        _engine = pyttsx3.init()
        _engine.setProperty("rate", 185)
        _engine.setProperty("volume", 0.95)
        # tenta voz PT-BR
        for v in _engine.getProperty("voices"):
            name = (v.name or "").lower()
            lang = "".join(v.languages).lower() if hasattr(v, "languages") else ""
            if "portuguese" in name and "brazil" in name:
                _engine.setProperty("voice", v.id); break
            if "pt" in lang and "br" in lang:
                _engine.setProperty("voice", v.id); break
    return _engine

async def _edge_say(texto: str, voice="pt-BR-FranciscaNeural", rate="+0%"):
    # Gera um MP3 temporário e toca com o próprio edge-tts (stream para arquivo)
    out = os.path.join(tempfile.gettempdir(), "bibigo_tts.mp3")
    communicate = edge_tts.Communicate(texto, voice=voice, rate=rate)
    await communicate.save(out)
    # tenta tocar com playsound ou pydub/simpleaudio se quiser.
    try:
        from playsound import playsound  # pip install playsound==1.2.2
        playsound(out)
    except Exception:
        # fallback: abre com player padrão do sistema (Windows)
        os.startfile(out)

def falar(texto: str):
    if EDGE_OK:
        try:
            asyncio.run(_edge_say(texto))
            return
        except Exception:
            pass  # se falhar, usa offline
    # fallback offline
    eng = _get_engine()
    eng.say(texto)
    eng.runAndWait()

def parar():
    if _engine:
        _engine.stop()
