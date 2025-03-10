from pymongo import MongoClient
import os

MONGO_URI = os.getenv("MONGO_URI")
client = MongoClient(MONGO_URI)
db = client["stock_market_db"]

def save_to_db(data, collection_name):
    """Save processed stock data to MongoDB."""
    collection = db[collection_name]
    collection.insert_many([data])
    print(f"[DB] Stored {len(data)} records in {collection_name}")

