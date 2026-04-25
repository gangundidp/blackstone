from backend.dataproviders.newsprovider import fetch_news
from backend.analysis.sentimentanalysis import analyze_sentiment


def get_news_with_sentiment(symbol: str):
    articles = fetch_news(symbol)

    enriched_news = []

    sentiments = []

    for article in articles:
        sentiment = analyze_sentiment(article["title"])
        sentiments.append(sentiment)

        enriched_news.append({
            "title": article["title"],
            "link": article["link"],
            "published": article["published"],
            "sentiment": sentiment
        })

    # Aggregate sentiment
    positive = sentiments.count("Positive")
    negative = sentiments.count("Negative")

    if positive > negative:
        overall = "Positive"
    elif negative > positive:
        overall = "Negative"
    else:
        overall = "Neutral"

    return {
        "articles": enriched_news,
        "overall_sentiment": overall
    }