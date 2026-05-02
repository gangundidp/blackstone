def map_symbol(symbol: str, region: str):
    symbol = symbol.upper()

    if region == "IN":
        return {
            "nse": symbol,
            "yahoo": f"{symbol}.NS",
            "moneycontrol": symbol.lower(),
            "screener": symbol.lower()
        }

    return {"default": symbol}