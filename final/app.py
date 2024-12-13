from flask import Flask, render_template, request, redirect, url_for
from utils.stock_data import get_stock_prices_from_api
from utils.currency_data import get_exchange_rates_from_api
from models.stock_model import get_historical_prices
from utils.analysis import analyze_trend
import requests
import os
from datetime import datetime, timedelta
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)

@app.template_filter('datetime')
def datetime_filter(unix_timestamp):
    """Convert Unix timestamp to human-readable date.
    
    Args:
        unix_timestamp (int): Unix timestamp to convert
        
    Returns:
        str: Formatted date string in YYYY-MM-DD HH:MM:SS format
    """
    return datetime.utcfromtimestamp(unix_timestamp).strftime('%Y-%m-%d %H:%M:%S')

@app.route('/')
def landing_page():
    """Render the landing page."""
    return render_template('landing.html')

@app.route('/dashboard')
def dashboard():
    """
    Render the dashboard with current stock prices and recommendations.
    Fetches latest stock prices and exchange rates, calculates currency-adjusted prices
    and generates trading recommendations.
    """
    stock_prices = get_stock_prices_from_api()
    exchange_rates = get_exchange_rates_from_api()
    stocks = []

    for stock in stock_prices:
        prices = {currency: stock['price'] * exchange_rates[currency] 
                 for currency in exchange_rates}
        recommendation = analyze_trend(stock['price'], 
                                     get_historical_prices(stock['ticker']))
        stocks.append({
            "ticker": stock['ticker'],
            "prices": prices,
            "recommendation": recommendation
        })

    return render_template('dashboard.html', stocks=stocks)

@app.route('/search', methods=['GET', 'POST'])
def search():
    """Handle stock search functionality.
    
    GET: Display search form
    POST: Redirect to company details page for entered ticker
    """
    if request.method == 'POST':
        ticker = request.form.get('ticker').strip().upper()
        return redirect(url_for('company_details', ticker=ticker))
    return render_template('search.html')

@app.route('/company/<ticker>')
def company_details(ticker):
    """
    Display detailed company information and recent news.
    
    Args:
        ticker (str): Stock ticker symbol
        
    Returns:
        rendered template with company profile and news data
    """
    finnhub_key = os.getenv("FINNHUB_API_KEY")
    
    # Calculate date range for news (last 7 days)
    today = datetime.utcnow()
    seven_days_ago = today - timedelta(days=7)
    date_format = '%Y-%m-%d'
    today_str = today.strftime(date_format)
    seven_days_ago_str = seven_days_ago.strftime(date_format)

    # Finnhub API endpoints
    base_url = f"https://finnhub.io/api/v1/stock/profile2?symbol={ticker}&token={finnhub_key}"
    news_url = f"https://finnhub.io/api/v1/company-news?symbol={ticker}&from={seven_days_ago_str}&to={today_str}&token={finnhub_key}"
    
    # Fetch data from Finnhub API
    profile_response = requests.get(base_url)
    news_response = requests.get(news_url)

    profile = profile_response.json() if profile_response.status_code == 200 else {}
    news = news_response.json() if news_response.status_code == 200 else []
    
    return render_template('company.html', profile=profile, news=news)

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=int(os.getenv('PORT', 8080)))
