import requests
from models.stock_model import save_stock_price
from dotenv import load_dotenv
import os
# Load environment variables
load_dotenv()

API_KEY= os.getenv("FINNHUB_API_KEY")
TOP_COMPANIES = [
    {"company": "Apple Inc.", "ticker": "AAPL"},
    {"company": "Microsoft Corp", "ticker": "MSFT"},
    {"company": "Alphabet Inc.", "ticker": "GOOGL"},
    {"company": "Amazon.com Inc.", "ticker": "AMZN"},
    {"company": "Tesla Inc.", "ticker": "TSLA"},
    {"company": "Meta Platforms Inc.", "ticker": "META"},
    {"company": "NVIDIA Corporation", "ticker": "NVDA"},
    {"company": "Berkshire Hathaway Inc.", "ticker": "BRK.B"},
    {"company": "Visa Inc.", "ticker": "V"},
    {"company": "Johnson & Johnson", "ticker": "JNJ"}
]

def get_stock_prices_from_api():
    """
    Fetch stock prices for the top companies from the Finnhub API and save to Datastore.
    """
    base_url = "https://finnhub.io/api/v1/quote"
    stock_data = []
    for company in TOP_COMPANIES:
        response = requests.get(f"{base_url}?symbol={company['ticker']}&token={API_KEY}")
        if response.status_code == 200:
            data = response.json()
            price = data['c']  # Current price
            save_stock_price(company['ticker'], price)  # Save to Datastore
            stock_data.append({'ticker': company['ticker'], 'price': price})
    return stock_data
