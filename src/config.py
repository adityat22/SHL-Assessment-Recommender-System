import os
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY not found in environment variables. Please check your .env file.")

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
SCRAPING_DIR = os.path.join(DATA_DIR, "scraping")
RAW_HTML_DIR = os.path.join(SCRAPING_DIR, "raw_html")
PARSED_DATA_PATH = os.path.join(DATA_DIR, "shl_products.json")

EMBEDDING_MODEL = "models/embedding-001"
GENERATION_MODEL = "gemini-pro"
