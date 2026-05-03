from functools import lru_cache

from backend.services.data_aggregator import DataAggregator
from backend.services.normalizer import Normalizer

aggregator = DataAggregator()
normalizer = Normalizer()


def safe_float(value):
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


@lru_cache(maxsize=100)
def fetch_complete_stock_data(symbol: str, region: str = "IN"):
    """
    Unified stock data fetcher (India-first architecture)
    """

    # STEP 1: Fetch from multiple sources
    raw_data = aggregator.fetch_all(symbol, region)

    # STEP 2: Normalize
    normalized = normalizer.normalize(raw_data, symbol, region)

    # STEP 3: Validation
    if not normalized.get("price"):
        raise ValueError(f"Invalid or unavailable stock data for symbol: {symbol}")

    return normalized