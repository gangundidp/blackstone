import yfinance as yf

def get_stock_data(symbol: str):
    stock = yf.Ticker(symbol)

    try:
        info = stock.info
    except Exception:
        return None

    return {
        "symbol": symbol,
        "price": info.get("currentPrice"),
        "pe": info.get("trailingPE"),
        "roe": info.get("returnOnEquity"),
        "market_cap": info.get("marketCap"),
        "sector": info.get("sector"),
    }