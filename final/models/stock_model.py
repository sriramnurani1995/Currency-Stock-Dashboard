from google.cloud import datastore
from datetime import datetime, timedelta
import os

# Initialize Datastore client
client = datastore.Client(project=os.getenv('GOOGLE_CLOUD_PROJECT'))

def save_stock_price(ticker, price):
    """
    Save stock price in Datastore.
    
    Args:
        ticker (str): Stock ticker symbol
        price (float): Current stock price
    """
    key = client.key('StockPrice')
    entity = datastore.Entity(key=key)
    entity.update({
        'price': price,
        'timestamp': datetime.utcnow(),
        'ticker': ticker
    })
    client.put(entity)

def get_historical_prices(ticker, days=30):
    """
    Retrieve historical stock prices for the given ticker.
    
    Args:
        ticker (str): Stock ticker symbol
        days (int): Number of days of historical data to retrieve
        
    Returns:
        list: List of historical prices ordered by timestamp
    """
    cutoff_date = datetime.utcnow() - timedelta(days=days)
    query = client.query(kind='StockPrice')
    query.add_filter('ticker', '=', ticker)
    query.add_filter('timestamp', '>=', cutoff_date)
    query.order = ['timestamp']
    
    return [entity["price"] for entity in query.fetch()]
