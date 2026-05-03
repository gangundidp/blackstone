import requests

class MoneycontrolAdapter:

    def fetch(self, symbol: str):
        try:
            # Placeholder — Moneycontrol requires mapping ISIN/code
            return {
                "source": "moneycontrol",
                "note": "integration pending proper mapping"
            }

        except Exception as e:
            return {"error": str(e)}