from typing import Dict, List, Optional
from datetime import datetime
from config.settings import AMERICA_RECIFE

"""
Contrato esperado pelo handler:
{
  "source": "stub|justtcg|...",
  "currency": "USD",
  "low": float|None,
  "avg": float|None,
  "market": float|None,
  "avg_30d": float|None,
  "confidence": float|None,  # 0..1 (opcional)
  "last_updated": "YYYY-MM-DD"  # data (local) usada para "promoções do dia"
}
"""

def obter_preco(card_name: str, card_number: str) -> Optional[Dict]:
    # compatibilidade retro com o handler antigo
    hoje = datetime.now(AMERICA_RECIFE).date().isoformat()
    if not card_number:
        return None
    # STUB determinístico pra testes
    base = sum(map(ord, (card_number or "X"))) % 20 + 5  # 5..24
    return {
        "source": "stub",
        "currency": "USD",
        "low": round(base * 0.9, 2),
        "avg": round(base, 2),
        "market": round(base * 0.95, 2),
        "avg_30d": round(base * 1.05, 2),
        "confidence": 0.8,
        "last_updated": hoje
    }

def obter_precos_em_lote(items: List[Dict]) -> List[Optional[Dict]]:
    """
    items: [{"name": str, "number": str}, ...]
    Retorna lista de preços no mesmo índice.
    """
    out = []
    for it in items:
        out.append(obter_preco(it.get("name",""), it.get("number","")))
    return out
