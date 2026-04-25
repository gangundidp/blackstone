from textblob import TextBlob

def analyze_sentiment(news_items):
    """
    news_items = [
        {"title": "...", "summary": "..."},
        ...
    ]
    """

    sentiments = []

    for item in news_items:
        text = f"{item.get('title', '')}. {item.get('summary', '')}"
        polarity = TextBlob(text).sentiment.polarity

        sentiments.append(polarity)

    if not sentiments:
        return {
            "score": 0,
            "label": "neutral"
        }

    avg_score = sum(sentiments) / len(sentiments)

    if avg_score > 0.2:
        label = "positive"
    elif avg_score < -0.2:
        label = "negative"
    else:
        label = "neutral"

    return {
        "score": round(avg_score, 3),
        "label": label
    }