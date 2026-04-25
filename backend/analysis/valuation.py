from backend.analysis.scoringengine import calculate_total_score, get_verdict


def basic_analysis(data: dict):
    pe = data.get("pe")
    roe = data.get("roe")

    # Phase 2 scoring system
    score_data = calculate_total_score(data)
    verdict = get_verdict(score_data["total_score"])

    return {
        "pe": pe,
        "roe": roe,
        "score": score_data["total_score"],
        "breakdown": score_data["breakdown"],
        "verdict": verdict
    }