import yfinance as yf

def get_stock_data(symbol: str):
    stock = yf.Ticker(symbol)

    info = stock.info
    financials = stock.financials

    return {
        "symbol": symbol,
        "currentPrice": info.get("currentPrice"),
        "trailingPE": info.get("trailingPE"),
        "returnOnEquity": info.get("returnOnEquity"),
        "debtToEquity": info.get("debtToEquity"),
        "revenueGrowth": info.get("revenueGrowth"),
        "profitMargins": info.get("profitMargins"),
    }