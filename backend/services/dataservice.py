def safe_float(value):
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


from backend.dataproviders.yahoofinance import get_stock_data
from functools import lru_cache

@lru_cache(maxsize=100)
def fetch_complete_stock_data(symbol: str):
    raw = get_stock_data(symbol)

    return {
        "symbol": symbol,
        "price": safe_float(raw.get("currentPrice")),
        "pe": safe_float(raw.get("trailingPE")),
        "roe": safe_float(raw.get("returnOnEquity")),
        "de_ratio": safe_float(raw.get("debtToEquity")),
        "revenue_growth": safe_float(raw.get("revenueGrowth")),
        "profit_margin": safe_float(raw.get("profitMargins")),
    }