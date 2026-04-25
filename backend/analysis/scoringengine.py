def score_pe(pe):
    if pe is None:
        return 0
    if pe < 15:
        return 3
    elif pe < 25:
        return 2
    elif pe < 40:
        return 1
    return 0

def score_roe(roe):
    if roe is None:
        return 0

    # Handle string inputs like "15%" or "15.2"
    if isinstance(roe, str):
        roe = roe.replace("%", "").strip()
        try:
            roe = float(roe)
        except:
            return 0

    # Normalize percentage → decimal
    if roe > 1:
        roe = roe / 100

    # Handle negative ROE explicitly
    if roe < 0:
        return 0

    # Scoring logic
    if roe > 0.20:
        return 3
    elif roe > 0.15:
        return 2
    elif roe > 0.10:
        return 1
    return 0


def calculate_total_score(data: dict):
    pe = data.get("pe")
    roe = data.get("roe")

    pe_score = score_pe(pe)
    roe_score = score_roe(roe)

    total_score = pe_score + roe_score

    return {
        "total_score": total_score,
        "breakdown": {
            "pe": pe_score,
            "roe": roe_score
        }
    }


def get_verdict(score):
    if score >= 5:
        return "Strong Buy"
    elif score >= 3:
        return "Buy"
    elif score >= 2:
        return "Hold"
    return "Avoid"