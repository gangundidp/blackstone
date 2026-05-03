from backend.analysis.factor_model import final_score


def analyze_fundamentals(data: dict):
    """
    Entry point for fundamental analysis.
    Uses multi-factor quantitative model.
    """

    result = final_score(data)

    return {
        "summary": result["rating"],
        "score": result["final_score"],
        "factors": result["factors"]
    }