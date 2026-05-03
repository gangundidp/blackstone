import yfinance as yf
from functools import lru_cache

@lru_cache(maxsize=100)
class YahooAdapter:

    def fetch(self, symbol: str):
        try:
            stock = yf.Ticker(symbol)
            info = stock.info

            return {
                "price": info.get("currentPrice"),
                "market_cap": info.get("marketCap"),
                "pe_ratio": info.get("trailingPE"),
                "pb_ratio": info.get("priceToBook"),

                "roe": info.get("returnOnEquity"),
                "de_ratio": info.get("debtToEquity"),
                "current_ratio": info.get("currentRatio"),

                "profit_margin": info.get("profitMargins"),
                "op_margin": info.get("operatingMargins"),

                "revenue_growth": info.get("revenueGrowth"),
                "profit_growth": info.get("earningsGrowth"),
            }

        except Exception as e:
            return {"error": str(e)}