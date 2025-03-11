import yfinance as yf
import pandas as pd

def fetch_stock_data(ticker: str, period: str = "5y") -> pd.DataFrame | None:
    """Fetches historical stock data for a given ticker."""
    try:
        stock = yf.Ticker(ticker)
        data = stock.history(period=period)
        return data
    except Exception as e:
        print(f"Error fetching stock data for {ticker}: {e}")
        return None