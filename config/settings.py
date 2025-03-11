import os
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
ALPHA_VANTAGE_API_KEY = os.getenv("ALPHA_VANTAGE_API_KEY")
NEWS_API_KEY = os.getenv("NEWS_API_KEY")
ECONOMIC_DATA_API_KEY = os.getenv("ECONOMIC_DATA_API_KEY")

MONGO_URI = os.getenv("MONGO_URI")
#POSTGRES_URI = os.getenv("POSTGRES_URI")

LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
