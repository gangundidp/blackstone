import re

def clean_percentage(value):
    if not value:
        return None

    if isinstance(value, (int, float)):
        return float(value)

    # Extract number from string like "65.2 %"
    match = re.search(r"[\d.]+", value)
    return float(match.group()) if match else None


def clean_number(value):
    if value is None:
        return None

    try:
        return float(value)
    except:
        return None

def pct_to_number(value):
    if value is None:
        return None
    return value * 100  # convert 0.65 → 65


class Normalizer:

    def normalize(self, raw_data: dict, symbol: str, region="IN"):

        nse = raw_data.get("nse", {})
        screener = raw_data.get("screener", {})
        yahoo = raw_data.get("yahoo", {})

        def pick(*values):
            for v in values:
                if v not in [None, "", "N/A"]:
                    return v
            return None

        return {
            "symbol": symbol,
            "region": region,

            "price": pick(nse.get("price"), yahoo.get("price")),

            "pe_ratio": pick(
                nse.get("pe_ratio"),
                screener.get("pe_ratio"),
                yahoo.get("pe_ratio")
            ),

            "pb_ratio": pick(
                screener.get("pb_ratio"),
                yahoo.get("pb_ratio")
            ),

            "market_cap": pick(
                nse.get("market_cap"),
                yahoo.get("market_cap")
            ),

            # QUALITY
            "roe": pick(
                screener.get("roe"),
                pct_to_number(yahoo.get("roe"))
            ),

            "roce": screener.get("roce"),

            "op_margin": pick(
                screener.get("op_margin"),
                pct_to_number(yahoo.get("op_margin"))
            ),

            # GROWTH
            "sales_growth": pick(
                screener.get("sales_growth"),
                pct_to_number(yahoo.get("revenue_growth"))
            ),

            "profit_growth": pick(
                screener.get("profit_growth"),
                pct_to_number(yahoo.get("profit_growth"))
            ),

            # RISK
            "de_ratio": pick(
                screener.get("de_ratio"),
                yahoo.get("de_ratio")
            ),

            "current_ratio": pick(
                screener.get("current_ratio"),
                yahoo.get("current_ratio")
            ),

            "sources": raw_data
        }