import requests
from models.exchange_model import save_exchange_rate
from dotenv import load_dotenv
import os
# Load environment variables
load_dotenv()

API_KEY= os.getenv("EXCHANGE_RATE_API_KEY")

def get_exchange_rates_from_api():
    """
    Fetch live exchange rates from the Currency API and save to Datastore.
    """
    base_url = "https://api.exchangerate-api.com/v4/latest/USD"
    response = requests.get(base_url)
    if response.status_code == 200:
        data = response.json()
        rates = {currency: data["rates"].get(currency, 0.0) for currency in ["USD", "EUR", "INR", "GBP"]}
        for currency, rate in rates.items():
            save_exchange_rate(currency, rate)  # Save to Datastore
        return rates
    return {"USD": 1.0, "EUR": 0.0, "INR": 0.0, "GBP": 0.0}

