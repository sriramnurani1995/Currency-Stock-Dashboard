import requests
from models.exchange_model import save_exchange_rate
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

def get_exchange_rates_from_api():
    """
    Fetch live exchange rates from the Exchange Rate API V6.
    
    Returns:
        dict: Dictionary of currency codes and their exchange rates
        
    Note:
        Requires EXCHANGE_RATE_API_KEY environment variable to be set
        with a valid API key from https://www.exchangerate-api.com/
    """
    api_key = os.getenv("EXCHANGE_RATE_API_KEY")
    if not api_key:
        raise ValueError("EXCHANGE_RATE_API_KEY environment variable is not set")
        
    base_url = f"https://v6.exchangerate-api.com/v6/{api_key}/latest/USD"
    response = requests.get(base_url)
    
    if response.status_code == 200:
        data = response.json()
        currencies = ["USD", "EUR", "INR", "GBP"]
        rates = {currency: data["conversion_rates"].get(currency, 0.0) for currency in currencies}
        
        for currency, rate in rates.items():
            save_exchange_rate(currency, rate)
        
        return rates
    
    return {"USD": 1.0, "EUR": 0.0, "INR": 0.0, "GBP": 0.0}
