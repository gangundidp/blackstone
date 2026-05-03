import requests
from bs4 import BeautifulSoup
import re


class ScreenerAdapter:

    BASE_URL = "https://www.screener.in/company"

    def _clean_value(self, text):
        if not text:
            return None

        text = text.replace(",", "").strip()

        # Extract numeric value
        match = re.search(r"-?\d+\.?\d*", text)
        if not match:
            return None

        return float(match.group())

    def fetch(self, symbol: str):
        try:
            url = f"{self.BASE_URL}/{symbol}/"
            headers = {"User-Agent": "Mozilla/5.0"}

            response = requests.get(url, headers=headers, timeout=5)
            soup = BeautifulSoup(response.text, "html.parser")

            ratios = {}

            for row in soup.select("li.flex.flex-space-between"):
                key = row.select_one("span.name").text.strip()
                value = row.select_one("span.value").text.strip()

                ratios[key] = self._clean_value(value)

            # Map to structured output
            return {
                "pe_ratio": ratios.get("P/E"),
                "pb_ratio": ratios.get("P/B"),
                "roe": ratios.get("ROE"),
                "roce": ratios.get("ROCE"),
                "div_yield": ratios.get("Dividend Yield"),
                "de_ratio": ratios.get("Debt to equity"),
                "current_ratio": ratios.get("Current ratio"),
                "sales_growth": ratios.get("Sales growth"),
                "profit_growth": ratios.get("Profit growth"),
                "op_margin": ratios.get("OPM"),
                "net_margin": ratios.get("NPM"),
            }

        except Exception as e:
            return {"error": str(e)}