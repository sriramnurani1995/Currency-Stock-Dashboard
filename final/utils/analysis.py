def calculate_moving_average(prices, period=7):
    """
    Calculate the moving average for the last 'period' prices.
    
    Args:
        prices (list): List of historical prices
        period (int): The number of days for the moving average
        
    Returns:
        float: The moving average or None if not enough data
    """
    if len(prices) < period:
        return None
    return sum(prices[-period:]) / period

def analyze_trend(current_price, historical_prices):
    """
    Analyze stock trends and provide a recommendation.
    
    Args:
        current_price (float): The current stock price
        historical_prices (list): List of historical prices (most recent last)
        
    Returns:
        str: "Buy", "Sell", or "Hold" recommendation
    """
    moving_average = calculate_moving_average(historical_prices)
    
    if moving_average is None:
        return "Hold"
        
    if current_price > moving_average:
        return "Buy"
    elif current_price < moving_average:
        return "Sell"
    
    return "Hold"
