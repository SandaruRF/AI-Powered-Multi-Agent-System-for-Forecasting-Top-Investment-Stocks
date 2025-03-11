import requests
import os
from typing import Dict, Any

def fetch_economic_data(indicator: str) -> Dict[str, Any] | None:
    """Fetches macroeconomic data for a given indicator."""
    api_key = os.getenv("ECONOMIC_DATA_API_KEY")
    url = f"https://api.example.com/economic-data?indicator={indicator}&apikey={api_key}"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Failed to fetch economic data: {response.status_code}")
            return None
    except Exception as e:
        print(f"Error fetching economic data: {e}")
        return None
