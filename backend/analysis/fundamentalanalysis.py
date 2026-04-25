def score_pe(pe):
    if pe is None:
        return 0
    if pe < 15: return 3
    elif pe < 25: return 2
    elif pe < 40: return 1
    return 0

def score_roe(roe):
    if roe is None:
        return 0
    roe = roe * 100
    if roe > 20: return 3
    elif roe > 15: return 2
    elif roe > 10: return 1
    return 0

def score_de(de):
    if de is None:
        return 0
    if de < 0.5: return 3
    elif de < 1: return 2
    elif de < 2: return 1
    return 0

def score_growth(growth):
    if growth is None:
        return 0
    growth = growth * 100
    if growth > 20: return 3
    elif growth > 10: return 2
    elif growth > 5: return 1
    return 0


def analyze_fundamentals(data: dict):
    scores = {
        "pe": score_pe(data.get("pe")),
        "roe": score_roe(data.get("roe")),
        "debt": score_de(data.get("de_ratio")),
        "growth": score_growth(data.get("revenue_growth")),
    }

    total_score = sum(scores.values())

    if total_score >= 10:
        rating = "Strong Buy"
    elif total_score >= 7:
        rating = "Buy"
    elif total_score >= 4:
        rating = "Hold"
    else:
        rating = "Avoid"

    return {
        "score": total_score,
        "rating": rating,
        "breakdown": scores
    }