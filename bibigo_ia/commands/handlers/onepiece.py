from features.onepiece.optcg_api import filtrar_promos, buscar_promo_por_id
from features.onepiece.precos_provider import obter_preco
from utils.fmt import formatar_preco

def handle_promocoes(query: str = "") -> str:
    """
    Se o usuário disser só 'promoções' -> mostra top 5 correspondências.
    Se passar algo como 'promoções luffy p-001' -> busca por id/termo e tenta trazer preço.
    """
    query = (query or "").strip()

    # Caso: o usuário forneceu um ID explícito tipo 'p-001'
    if query and any(c in query for c in ["p-", "op", "eb", "st"]):
        card = buscar_promo_por_id(query.upper())
        nome = card.get("name") or card.get("card_name") or "Carta"
        numero = card.get("number") or card.get("card_id") or query.upper()
        preco = obter_preco(nome, numero)
        return f"{nome} ({numero}) — {formatar_preco(preco)}"

    # Caso genérico: fuzzy search entre as promos
    resultados = filtrar_promos(query, limit=5)
    if not resultados:
        return "Não encontrei promoções correspondentes."

    linhas = []
    for p in resultados:
        nome = p.get("name") or "?"
        numero = p.get("number") or p.get("card_id") or "?"
        preco = obter_preco(nome, numero)
        linhas.append(f"- {nome} ({numero}) → {formatar_preco(preco)}")
    return "Promoções (PROMO) que encontrei:\n" + "\n".join(linhas)
