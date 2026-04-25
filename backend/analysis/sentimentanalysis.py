POSITIVE_WORDS = [
    "growth", "profit", "gain", "surge", "beat", "strong", "expansion"
]

NEGATIVE_WORDS = [
    "loss", "decline", "drop", "fall", "weak", "debt", "crisis"
]


def analyze_sentiment(text: str):
    text = text.lower()

    pos_score = sum(word in text for word in POSITIVE_WORDS)
    neg_score = sum(word in text for word in NEGATIVE_WORDS)

    if pos_score > neg_score:
        return "Positive"
    elif neg_score > pos_score:
        return "Negative"
    return "Neutral"