from google.cloud import datastore
from datetime import datetime

client = datastore.Client(project="cloud-nurani-srirams")

def save_exchange_rate(currency, rate):
    """
    Save or update exchange rate in Datastore.
    """
    key = client.key('ExchangeRate')
    entity = datastore.Entity(key=key)
    entity.update({
        'rate': rate,
        'timestamp': datetime.utcnow()
    })
    client.put(entity)

def get_exchange_rates():
    """
    Retrieve the latest exchange rates from Datastore.
    """
    query = client.query(kind='ExchangeRate')
    rates = {}
    for entity in query.fetch():
        rates[entity.key.name] = entity['rate']
    return rates
