def formatar_preco(p):
    if not p:
        return "Sem preço disponível na fonte configurada."
    parts = []
    if p.get("low") is not None: parts.append(f"low {p['low']} {p['currency']}")
    if p.get("avg") is not None: parts.append(f"avg {p['avg']} {p['currency']}")
    if p.get("market") is not None: parts.append(f"market {p['market']} {p['currency']}")
    src = p.get("source","?")
    return f"{' | '.join(parts)} (fonte: {src})"

