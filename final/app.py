from flask import Flask, render_template
from utils.stock_data import get_stock_prices_from_api
from utils.currency_data import get_exchange_rates_from_api
from models.stock_model import get_historical_prices
from models.exchange_model import get_exchange_rates
from utils.analysis import analyze_trend

app = Flask(__name__)

@app.route('/dashboard')
def dashboard():
    # Fetch and store stock prices and exchange rates
    stock_data = get_stock_prices_from_api()
    exchange_rates = get_exchange_rates_from_api()

    # Prepare data for the dashboard
    currencies = ["USD", "EUR", "INR", "GBP"]
    processed_data = []
    for stock in stock_data:
        ticker = stock['ticker']
        current_price = stock['price']

        # Get historical prices for trend analysis
        historical_prices = get_historical_prices(ticker)
        print(f"Ticker: {ticker}, Current Price: {current_price}, Historical Prices: {historical_prices}")

        # Analyze trends and generate recommendations
        recommendation = analyze_trend(current_price, historical_prices)

        # Calculate currency-adjusted prices
        prices_in_currencies = {currency: current_price * exchange_rates[currency] for currency in currencies}

        processed_data.append({
            'ticker': ticker,
            'prices': prices_in_currencies,
            'recommendation': recommendation
        })

    return render_template('dashboard.html', stocks=processed_data, currencies=currencies)

# Landing Page Route
@app.route('/')
def landing():
    return render_template('landing.html')

if __name__ == "__main__":
    app.run(debug=True)
