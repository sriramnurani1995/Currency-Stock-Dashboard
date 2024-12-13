from google.cloud import datastore
from datetime import datetime
import os

# Initialize Datastore client
client = datastore.Client(project=os.getenv('GOOGLE_CLOUD_PROJECT'))

def save_exchange_rate(currency, rate):
    """
    Save exchange rate in Datastore.
    
    Args:
        currency (str): Currency code (e.g., 'USD', 'EUR')
        rate (float): Exchange rate value
    """
    key = client.key('ExchangeRate', currency)
    entity = datastore.Entity(key=key)
    entity.update({
        'rate': rate,
        'timestamp': datetime.utcnow()
    })
    client.put(entity)
