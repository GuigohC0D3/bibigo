# commands/handlers/onepiece.py
from features.onepiece.optcg_api import (
    listar_decks,
    filtrar_decks,
    listar_cartas_de_deck,
    filtrar_cartas_de_deck,
    buscar_carta_deck_por_id,
)
from features.onepiece.precos_provider import obter_preco, obter_precos_em_lote
from utils.fmt import formatar_preco

def handle_listar_decks(query: str = "", limit: int = 10) -> str:
    """
    Lista decks (starter) – se query vier, faz fuzzy e retorna top-N.
    """
    query = (query or "").strip()
    if query:
        decks = filtrar_decks(query, limit=limit)
    else:
        decks = listar_decks()[:limit]

    if not decks:
        return "Não encontrei nenhum deck correspondente."

    linhas = []
    for d in decks:
        nome = d.get("name") or d.get("productName") or d.get("product_name") or "Deck"
        stid = d.get("st_id") or d.get("deck_id") or "?"
        linhas.append(f"- {nome} ({stid})")
    return "Decks encontrados:\n" + "\n".join(linhas)

def handle_cartas_do_deck(st_id: str, query: str = "", limit: int = 10) -> str:
    """
    Lista cartas de um deck específico (ST-XX). Se query vier, fuzzy dentro do deck.
    Também tenta trazer preços (provider) quando possível.
    """
    st_id = (st_id or "").strip().upper()
    if not st_id:
        return "Qual o código do deck? Ex.: ST-01."

    if query:
        cartas = filtrar_cartas_de_deck(st_id, query, limit=limit)
    else:
        cartas = listar_cartas_de_deck(st_id)[:limit]

    if not cartas:
        return f"Não encontrei cartas no deck {st_id}."

    # preços em lote (seu provider faz stub por enquanto)
    items = [{"name": c.get("name",""), "number": c.get("number") or c.get("card_id") or ""} for c in cartas]
    precos = obter_precos_em_lote(items)

    linhas = []
    for c, p in zip(cartas, precos):
        nome = c.get("name") or "?"
        numero = c.get("number") or c.get("card_id") or "?"
        linhas.append(f"- {nome} ({numero}) → {formatar_preco(p)}")
    return f"Cartas do {st_id}:\n" + "\n".join(linhas)

def handle_carta_por_id(card_id: str) -> str:
    """
    Busca uma carta de deck pelo card_id (ex.: 'ST01-001' etc.) e mostra preço.
    """
    card_id = (card_id or "").strip().upper()
    if not card_id:
        return "Qual o ID da carta? Ex.: ST01-001."
    c = buscar_carta_deck_por_id(card_id)
    if not c:
        return f"Não encontrei a carta {card_id} nos decks."
    nome = c.get("name") or "Carta"
    numero = c.get("number") or c.get("card_id") or card_id
    preco = obter_preco(nome, numero)
    return f"{nome} ({numero}) — {formatar_preco(preco)}"
