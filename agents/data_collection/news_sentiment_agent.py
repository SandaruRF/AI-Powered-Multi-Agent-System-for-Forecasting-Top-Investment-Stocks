from newsapi import NewsApiClient
import os
from typing import List, Dict, Any

def fetch_news_sentiment(query: str) -> List[Dict[str, Any]]:
    """Fetches news articles and analyzes sentiment for a given query."""
    api_key = os.getenv("NEWS_API_KEY")
    newsapi = NewsApiClient(api_key=api_key)
    try:
        articles = newsapi.get_everything(q=query, language="en", sort_by="publishedAt")
        return articles["articles"]
    except Exception as e:
        print(f"Error fetching news for {query}: {e}")
        return []