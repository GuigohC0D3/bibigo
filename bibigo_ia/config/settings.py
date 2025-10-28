from datetime import timedelta, timezone

# timezone de Recife (UTC-3 sem DST)
AMERICA_RECIFE = timezone(timedelta(hours=-3))

LANG = "pt-BR"

# Lógica de “promo do dia”
DEAL_MIN_DISCOUNT_PCT = 0.15   # 15% abaixo da referência (avg_30d/market)
DEAL_MIN_CONFIDENCE   = 0.60   # score mínimo se a fonte fornecer confiança
MAX_DEALS             = 10     # máximo de itens listados

# Provedor de preços
PRICE_PROVIDER = "stub"  # depois troque para "justtcg" (ou o que você plugar)
