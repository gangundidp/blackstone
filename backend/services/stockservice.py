from dataEngine.collectors.yahoocollector import get_stock_data
from backend.analysis.valuation import basic_analysis

def analyze_stock(symbol: str):
    try:
        data = get_stock_data(symbol)

        if not data or data.get("price") is None:
            return {"error": "Invalid stock symbol or no data found"}

        analysis = basic_analysis(data)

        return {
            "symbol": symbol,
            "data": data,
            "analysis": analysis
        }

    except Exception as e:
        return {"error": str(e)}