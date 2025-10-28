# commands/router.py
from .handlers.basic import handle_basic
from .handlers.onepiece import (
    handle_listar_decks,
    handle_cartas_do_deck,
    handle_carta_por_id,
)

WAKE = "bibigo"

def _strip_wake(texto: str) -> str:
    t = (texto or "").lower()
    return t.replace(WAKE, "").strip() if WAKE in t else t.strip()

def rotear(texto: str) -> str:
    t = _strip_wake(texto)

    # Intent: listar decks (ex.: "listar decks", "decks do luffy")
    if ("deck" in t or "decks" in t) and ("listar" in t or "mostrar" in t or "ver" in t):
        # extrai uma possível query depois da palavra 'decks'
        # ex.: "mostrar decks do luffy" -> "luffy"
        q = t
        for gat in ["listar", "mostrar", "ver", "decks", "deck", "do", "da", "de"]:
            q = q.replace(gat, "")
        q = q.strip()
        return handle_listar_decks(q)  # q pode ser vazio

    # Intent: cartas de um deck específico (ex.: "cartas do ST-01", "listar cartas do ST-10 zoro")
    if "cartas" in t and ("st-" in t or "st" in t):
        # pegar o st_id
        # simplista: procura token que comece por "st"
        tokens = t.replace(",", " ").replace(".", " ").split()
        st_id = next((x.upper() for x in tokens if x.startswith("st")), "")
        # resto vira query dentro do deck
        q = " ".join([tok for tok in tokens if tok.lower() not in ["cartas", "do", "da", st_id.lower()]])
        return handle_cartas_do_deck(st_id, q.strip())

    # Intent: carta por ID direto (ex.: "carta ST01-001", "mostrar ST10-005")
    if any(k in t for k in ["st01-", "st02-", "st03-", "st04-", "st05-", "st06-", "st07-", "st08-", "st09-", "st10-", "st11-", "st12-", "st13-", "st14-", "st15-"]):
        # pegue o token que parece ID
        tokens = t.replace(",", " ").replace(".", " ").split()
        cid = next((x.upper() for x in tokens if "-" in x and x.lower().startswith("st")), "")
        if cid:
            return handle_carta_por_id(cid)

    # fallback: comandos básicos
    return handle_basic(t)
