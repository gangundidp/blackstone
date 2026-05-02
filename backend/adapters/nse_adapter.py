import requests

class NSEAdapter:

    BASE_URL = "https://www.nseindia.com/api/quote-equity"

    def fetch(self, symbol: str):
        try:
            headers = {
                "User-Agent": "Mozilla/5.0"
            }

            url = f"{self.BASE_URL}?symbol={symbol}"

            response = requests.get(url, headers=headers, timeout=5)
            data = response.json()

            return {
                "price": data.get("priceInfo", {}).get("lastPrice"),
                "market_cap": data.get("marketDeptOrderBook", {}).get("tradeInfo", {}).get("marketCap"),
                "pe_ratio": data.get("metadata", {}).get("pdSectorPe")
            }

        except Exception as e:
            return {"error": str(e)}