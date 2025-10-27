# commands/router.py
from commands.handlers.basic import handle_basic
from commands.handlers.onepiece import handle_promocoes

WAKE = "bibigo"

def _strip_wake(texto: str) -> str:
    t = (texto or "").lower()
    return t.replace(WAKE, "").strip() if WAKE in t else t.strip()

def rotear(texto: str) -> str:
    """
    Decide qual handler chamar.
    Retorna texto a ser falado. Se retornar '__EXIT__', o app encerra.
    """
    t = _strip_wake(texto)

    # One Piece (promoções)
    if "promo" in t and ("one piece" in t or "optcg" in t or "cartas" in t):
        # passa o restante como consulta (ex.: "luffy p-001")
        lixo = ["de", "do", "da", "one piece", "optcg", "cartas", "promoções", "promocoes", "promo", "promos"]
        q = " ".join([w for w in t.split() if w not in lixo]).strip()
        return handle_promocoes(q)

    # Básico (hora, youtube, pesquisar, wikipedia, tocar...)
    return handle_basic(t)
    