import requests
import pandas as pd
import yfinance as yf
from utils.api_helpers import fetch_stock_data, fetch_news_sentiment
from utils.db_helpers import save_to_db

class FinancialDataAggregationAgent:
    """Agent responsible for collecting, preprocessing, and storing stock market data."""

    def __init__(self, stock_symbols):
        self.stock_symbols = stock_symbols
        self.raw_data = {}
        self.preprocessed_data = {}

    def fetch_market_data(self):
        """Fetch historical stock prices using Yahoo Finance API."""
        print("[INFO] Fetching market data...")
        for symbol in self.stock_symbols:
            try:
                stock = yf.Ticker(symbol)
                df = stock.history(period="1y")
                self.raw_data[symbol] = df
                print(f"[SUCCESS] Fetched data for {symbol}")
            except Exception as e:
                print(f"[ERROR] Failed to fetch data for {symbol}: {e}")
                
    def fetch_fundamental_data(self):
        """Fetch financial statements, balance sheets, and cash flows"""
        print("[INFO] Fetching fundamental data...")
        for symbol in self.stock_symbols:
            try:
                data = fetch_stock_data(symbol) # Custom function from api_helpers.py
                self.raw_data[symbol + "_fundamentals"] = data
                print(f"[SUCCESS] Fetched fundamentals for {symbol}")
            except Exception as e:
                print(f"[ERROR] Failed to fetch fundamentals for {symbol}: {e}")

    def fetch_sentiment_data(self):
        """Fetch news sentiment analysis for market trends."""
        print("[INFO] Fetching sentiment data...")
        sentiment_data = fetch_news_sentiment(self.stock_symbols)
        self.raw_data["sentiment"] = sentiment_data

    def preprocess_data(self):
        """Clean and structure the collected data for further analysis."""
        print("[INFO] Preprocessing data...")
        for symbol, df in self.raw_data.items():
            if isinstance(df, pd.DataFrame):
                df.dropna(inplace=True)
                df.reset_index(inplace=True)
                self.processed_data[symbol] = df

    def store_data(self):
        """Store processed data in the database."""
        print("[INFO] Storing data to database...")
        save_to_db(self.processed_data, collection_name="stock_data")

    def run(self):
        """Execute the full data pipeline."""
        self.fetch_market_data()
        self.fetch_fundamental_data()
        self.fetch_sentiment_data()
        self.preprocess_data()
        self.store_data()

if __name__ == "__main__":
    agent = FinancialDataAggregationAgent(["AAPL", "GOOG", "TSLA"])
    agent.run()
