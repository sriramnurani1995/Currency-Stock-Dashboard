def calculate_moving_average(prices, period=7):
    """
    Calculate the moving average for the last 'period' prices.

    Args:
        prices (list): List of historical prices.
        period (int): The number of days for the moving average.

    Returns:
        float: The moving average or None if not enough data.
    """
    if len(prices) < period:
        return None  # Not enough data for the given period
    return sum(prices[-period:]) / period


def analyze_trend(current_price, historical_prices):
    """
    Analyze stock trends and provide a recommendation.

    Args:
        current_price (float): The current stock price.
        historical_prices (list): List of historical prices (most recent last).

    Returns:
        str: "Buy", "Sell", or "Hold" recommendation.
    """

    # Calculate the 7-day moving average
    moving_average = calculate_moving_average(historical_prices)
    if moving_average is None:
        print(f"Not enough data to calculate moving average for prices: {historical_prices}")
        return "Hold"  # Default to "Hold" if no moving average can be calculated
    # Recommendation logic based on comparison with moving average
    if current_price > moving_average:
        return "Buy"
    elif current_price < moving_average:
        return "Sell"
    else:
        return "Hold"
