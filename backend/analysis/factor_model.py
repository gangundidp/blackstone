def normalize_score(value, thresholds, reverse=False):
    """
    Generic scoring:
    thresholds = [(limit, score), ...]
    """
    if value is None:
        return 0

    for limit, score in thresholds:
        if (value <= limit and reverse) or (value >= limit and not reverse):
            return score

    return 0

def score_value(data):
    pe = data.get("pe_ratio")
    pb = data.get("pb_ratio")

    pe_score = normalize_score(pe, [(15, 3), (25, 2), (40, 1)], reverse=True)
    pb_score = normalize_score(pb, [(1, 3), (3, 2), (6, 1)], reverse=True)

    return (pe_score + pb_score) / 2

def score_quality(data):
    roe = data.get("roe")
    roce = data.get("roce")
    opm = data.get("op_margin")

    roe_score = normalize_score(roe, [(20, 3), (15, 2), (10, 1)])
    roce_score = normalize_score(roce, [(20, 3), (15, 2), (10, 1)])
    margin_score = normalize_score(opm, [(25, 3), (15, 2), (10, 1)])

    return (roe_score + roce_score + margin_score) / 3

def score_growth(data):
    sales = data.get("sales_growth")
    profit = data.get("profit_growth")

    sales_score = normalize_score(sales, [(20, 3), (10, 2), (5, 1)])
    profit_score = normalize_score(profit, [(20, 3), (10, 2), (5, 1)])

    return (sales_score + profit_score) / 2

def score_risk(data):
    de = data.get("de_ratio")
    current = data.get("current_ratio")

    de_score = normalize_score(de, [(0.5, 3), (1, 2), (2, 1)], reverse=True)
    current_score = normalize_score(current, [(2, 3), (1.5, 2), (1, 1)])

    return (de_score + current_score) / 2

def final_score(data):
    value = score_value(data)
    quality = score_quality(data)
    growth = score_growth(data)
    risk = score_risk(data)

    total = (
        value * 0.25 +
        quality * 0.35 +
        growth * 0.25 +
        risk * 0.15
    )

    if total >= 2.5:
        rating = "Strong Buy"
    elif total >= 2.0:
        rating = "Buy"
    elif total >= 1.5:
        rating = "Hold"
    else:
        rating = "Avoid"

    return {
        "final_score": round(total, 2),
        "rating": rating,
        "factors": {
            "value": round(value, 2),
            "quality": round(quality, 2),
            "growth": round(growth, 2),
            "risk": round(risk, 2)
        }
    }