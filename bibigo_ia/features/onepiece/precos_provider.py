from typing import Optional, Dict

def obter_preco(card_name: str, card_number: str) -> Optional[Dict]:
    """
    STUB de preços. Substitua por chamadas reais (ex.: JustTCG) cruzando por nome/number.
    Retorne sempre no formato padronizado abaixo.
    """
    # Exemplo fictício só para ver fluxo funcionando:
    if not card_number:
        return None
    return {
        "source": "stub",
        "currency": "USD",
        "low": 4.99,
        "avg": 7.49,
        "market": 6.90,
        "last_updated": "now"
    }
