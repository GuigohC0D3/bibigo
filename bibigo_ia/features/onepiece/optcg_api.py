import requests
from rapidfuzz import process, fuzz

BASE = "https://optcgapi.com"

def _get_json(path: str):
    r = requests.get(f"{BASE}{path}", timeout=30)
    r.raise_for_status()
    return r.json()

def listar_promos():
    """Lista todas as cartas PROMO (segundo a doc da OPTCG API)."""
    return _get_json("/api/allPromoCards")

def buscar_promo_por_id(card_id: str):
    """
    card_id ex.: 'P-001'.
    Algumas cartas podem estar em 'sets' ou 'decks'. Tentamos set e depois deck.
    """
    try:
        return _get_json(f"/api/sets/card/{card_id}/")
    except requests.HTTPError:
        return _get_json(f"/api/decks/card/{card_id}/")

def filtrar_promos(query: str, limit=10):
    """Busca fuzzy por nome/numero/id entre as promos."""
    promos = listar_promos()
    chaves = []
    for p in promos:
        chave = f"{p.get('card_id','')} {p.get('number','')} {p.get('name','')}"
        chaves.append((chave, p))
    matches = process.extract(
        query,
        [k for k,_ in chaves],
        scorer=fuzz.WRatio,
        limit=limit
    )
    out = []
    for text, score, idx in matches:
        out.append({"score": score, **chaves[idx][1]})
    return out
