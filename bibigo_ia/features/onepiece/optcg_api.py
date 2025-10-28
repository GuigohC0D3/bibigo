# features/onepiece/optcg_api.py
import requests
from rapidfuzz import process, fuzz

BASE = "https://optcgapi.com"

# sessão com timeout e cabeçalhos amigáveis
_session = requests.Session()
_session.headers.update({
    "User-Agent": "BIBIGO/1.0 (+https://github.com/GuigohC0D3)",
    "Accept": "application/json",
})

def _get_json(path: str):
    """
    Tenta com e sem barra final para evitar 404 de DRF.
    """
    url1 = f"{BASE}{path}"
    url2 = f"{BASE}{path if path.endswith('/') else path + '/'}"
    r = _session.get(url1, timeout=30)
    if r.status_code == 404 and not path.endswith('/'):
        r = _session.get(url2, timeout=30)
    r.raise_for_status()
    return r.json()

# -----------------------------
#            DECKS
# -----------------------------

def listar_decks():
    """Lista todos os Decks (Starter Decks)."""
    return _get_json("/api/allDecks/")

def listar_cartas_de_deck(st_id: str):
    """
    Retorna as cartas de um deck específico.
    Ex.: st_id = 'ST-01', 'ST-10', etc.
    """
    return _get_json(f"/api/decks/{st_id.upper()}/")

def buscar_carta_deck_por_id(card_id: str):
    """
    Busca uma carta (que pertence a um deck) pelo card_id.
    Ex.: 'ST01-001' (formato pode variar na API).
    """
    return _get_json(f"/api/decks/card/{card_id.upper()}/")

def filtrar_decks(query: str, limit=10):
    """
    Busca fuzzy entre os decks por nome/ID.
    Retorna lista com 'score' para permitir rankear resultados.
    """
    decks = listar_decks()
    chaves = []
    for d in decks:
        chave = " ".join([
            str(d.get("st_id", "")),
            str(d.get("deck_id", "")),
            str(d.get("name", "")),
            str(d.get("productName", "")),
            str(d.get("product_name", "")),
        ]).strip()
        chaves.append((chave, d))

    if not query:
        return decks[:limit]

    matches = process.extract(
        query,
        [k for k, _ in chaves],
        scorer=fuzz.WRatio,
        limit=limit
    )
    out = []
    for text, score, idx in matches:
        out.append({"score": score, **chaves[idx][1]})
    return out

def filtrar_cartas_de_deck(st_id: str, query: str, limit=10):
    """
    Fuzzy nas cartas de um deck específico.
    """
    cartas = listar_cartas_de_deck(st_id)
    chaves = []
    for c in cartas:
        chave = " ".join([
            str(c.get("card_id", "")),
            str(c.get("number", "")),
            str(c.get("name", "")),
            str(c.get("rarity", "")),
        ]).strip()
        chaves.append((chave, c))

    if not query:
        return cartas[:limit]

    matches = process.extract(
        query,
        [k for k, _ in chaves],
        scorer=fuzz.WRatio,
        limit=limit
    )
    out = []
    for text, score, idx in matches:
        out.append({"score": score, **chaves[idx][1]})
    return out
