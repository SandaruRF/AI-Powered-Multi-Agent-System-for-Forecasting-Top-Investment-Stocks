import yfinance as yf

class StockDataAgent:
    def __init__(self, ticker):
        self.ticker = ticker

    def fetch_stock_data(self, period="1y"):
        try:
            stock = yf.Ticker(self.ticker)
            data = stock.history(period=period)
            return data
        except Exception as e:
            print(f"Error fetching stock data for {self.ticker}: {e}")
            return None