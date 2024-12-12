from meteostat import Point, Hourly
from datetime import datetime

def fetch_and_save_weather_csv():
    """Fetch historical weather data for SFO and save as a CSV."""
    # Define SFO coordinates (latitude, longitude, and elevation)
    sfo = Point(37.7749, -122.4194)

    # Define time range
    start = datetime(2022, 1, 1)  # Start date
    end = datetime(2024, 12, 10)  # End date

    # Fetch hourly weather data
    data = Hourly(sfo, start, end)
    data = data.fetch()

    # Save the data to a CSV file
    data.to_csv("sfo_hourly_weather.csv")
    print("Weather data saved to 'sfo_hourly_weather.csv'")

if __name__ == "__main__":
    fetch_and_save_weather_csv()
