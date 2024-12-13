from google.cloud import datastore
from datetime import datetime, timedelta

client = datastore.Client(project="cloud-nurani-srirams")

def save_stock_price(ticker, price):
    """
    Save or update stock price in Datastore.
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
    Retrieve historical stock prices for the given ticker from the last 'days'.
    """
    print(ticker)
    cutoff_date = datetime.utcnow() - timedelta(days=days)
    query = client.query(kind='StockPrice')
    query.add_filter('ticker', '=', ticker)
    query.add_filter('timestamp', '>=', cutoff_date)
    query.order = ['timestamp']  # Order by oldest first
    results = list(query.fetch())
    historical_prices = [entity["price"] for entity in results]
    return historical_prices
