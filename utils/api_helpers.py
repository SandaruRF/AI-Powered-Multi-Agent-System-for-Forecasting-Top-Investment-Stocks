import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import requests
import os

ALPHA_VANTAGE_API_KEY = os.getenv("ALPHA_VANTAGE_API_KEY")

# Load finBERT model and tokenizer
MODEL_NAME = "yiyanghkust/finbert-tone"
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForSequenceClassification.from_pretrained(MODEL_NAME)

NEWS_API_KEY = os.getenv("NEWS_API_KEY")

def fetch_stock_data(symbol):
    """Fetch fundamental stock data from Alpha Vantage."""
    url = f"https://www.alphavantage.co/query?function=OVERVIEW&symbol={symbol}&apikey={ALPHA_VANTAGE_API_KEY}"
    response = requests.get(url)
    return response.json() if response.status_code == 200 else None

def fetch_news_articles(symbol):
    """Fetch recent news articles related to a stock symbol using NewsAPI."""
    url = f"https://newsapi.org/v2/everything?q={symbol}&language=en&sortBy=publishedAt&apiKey={NEWS_API_KEY}"
    response = requests.get(url)

    if response.status_code == 200:
        articles = response.json().get("articles", [])
        return [article["title"] + " " + article["description"] for article in articles if article["description"]]
    else:
        print(f"[ERROR] Failed to fetch news for {symbol}: {response.status_code}")
        return []

def analyze_sentiment_roberta(texts):
    """Analyze sentiment using FinBERT (RoBERTa)."""
    sentiment_scores = []

    for text in texts:
        inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True, max_length=512)
        with torch.no_grad():
            outputs = model(**inputs)

        logits = outputs.logits
        probs = torch.nn.functional.softmax(logits, dim=-1)
        sentiment_scores.append(probs.numpy().tolist()[0]) # Convert tensor to list

    # Average sentiment scores
    if sentiment_scores:
        avg_scores = torch.tensor(sentiment_scores).mean(dim=0)
        sentiment_class = ["Negative", "Neutral", "Positive"]
        return sentiment_class[torch.argmax(avg_scores).item()]
    
    return "Neutral"  # Default if no news articles found

def fetch_news_sentiment(symbols):
    """Fetch sentiment analysis for stock-related news using FinBERT."""
    sentiment_results = {}
    
    for symbol in symbols:
        print(f"[INFO] Fetching news for {symbol}...")
        articles = fetch_news_articles(symbol)

        if articles:
            sentiment = analyze_sentiment_roberta(articles)
            sentiment_results[symbol] = sentiment
        else:
            sentiment_results[symbol] = "No news articles found"
    
    return {"sentiment_analysis": sentiment_results}
