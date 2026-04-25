def generate_explanation(data: dict, analysis: dict):
    explanation = f"""
Stock Analysis Summary for {data['symbol']}:

- Current Price: {data.get('price')}
- PE Ratio: {data.get('pe')}
- ROE: {data.get('roe')}
- Debt/Equity: {data.get('de_ratio')}
- Revenue Growth: {data.get('revenue_growth')}

Overall Score: {analysis['score']}
Rating: {analysis['rating']}

Insights:
"""

    if analysis["breakdown"]["roe"] >= 2:
        explanation += "- Strong profitability (good ROE)\n"

    if analysis["breakdown"]["debt"] >= 2:
        explanation += "- Healthy debt levels\n"

    if analysis["breakdown"]["growth"] >= 2:
        explanation += "- Good revenue growth\n"

    if analysis["breakdown"]["pe"] <= 1:
        explanation += "- Stock may be overvalued\n"

    return explanation.strip()