import requests
import os
from typing import Dict, Any
from config.settings import ALPHA_VANTAGE_API_KEY

def fetch_fundamentals(ticker: str) -> Dict[str, Any] | None:
    """Fetches fundamental data for a given ticker."""
    api_key = ALPHA_VANTAGE_API_KEY
    url = f"https://www.alphavantage.co/query?function=OVERVIEW&symbol={ticker}&apikey={api_key}"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Failed to fetch fundamentals for {ticker}: {response.status_code}")
            return None
    except Exception as e:
        print(f"Error fetching fundamentals for {ticker}: {e}")
        return None
