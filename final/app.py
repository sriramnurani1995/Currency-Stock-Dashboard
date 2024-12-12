from flask import Flask, render_template, request
from api.predict_api import predict_delay
from api.weather_api import fetch_weather_data
from api.flights_api import fetch_flight_data

app = Flask(__name__)

# Landing Page
@app.route("/")
def index():
    return render_template("index.html")

# Prediction API
@app.route("/predict", methods=["POST"])
def predict():
    flight_info = request.form["flight_info"]
    date = request.form["date"]
    prediction = predict_delay(flight_info, date)
    return render_template("index.html", prediction=prediction)

# Dashboard
@app.route("/dashboard")
def dashboard():
    weather = fetch_weather_data()
    flights = fetch_flight_data()
    return render_template("dashboard.html", weather=weather, flights=flights)

if __name__ == "__main__":
    app.run(debug=True)
