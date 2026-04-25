import feedparser
import urllib.parse

def fetch_news(symbol: str):
    try:
        query = f"{symbol} stock"
        encoded_query = urllib.parse.quote(query)

        url = f"https://news.google.com/rss/search?q={encoded_query}"
        feed = feedparser.parse(url)

        articles = []

        for entry in feed.entries[:5]:
            articles.append({
                "title": entry.title,
                "link": entry.link,
                "published": entry.published
            })

        return articles

    except Exception:
        return []