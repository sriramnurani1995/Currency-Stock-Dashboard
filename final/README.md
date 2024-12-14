# Stock Market Dashboard

A Flask-based web application that provides real-time stock prices with currency conversion and trading recommendations.

## Features

- Real-time stock prices for top 10 companies
- Multi-currency support (USD, EUR, INR, GBP)
- Trading recommendations based on moving averages
- Company profiles and latest news
- Search functionality for any listed company

## Prerequisites

- Python 3.8 or higher
- Google Cloud SDK
- Docker
- Access to Google Cloud Platform (GCP)
- API Keys:
  - Finnhub API ([Get here](https://finnhub.io/))
  - Exchange Rate API V6 ([Get here](https://www.exchangerate-api.com/))

## Local Development Setup

1. Clone the repository:

```bash
git clone <repository-url>
cd stock-dashboard
```

2. Create and activate a virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the root directory:

```plaintext
FINNHUB_API_KEY=your_finnhub_api_key
EXCHANGE_RATE_API_KEY=your_exchange_rate_api_key
GOOGLE_CLOUD_PROJECT=your-gcp-project-id
PORT=8080
```

5. Run the application:

```bash
python app.py
```

Visit http://localhost:8080 to access the application.

## Code Documentation

### Main Application (app.py)

The Flask application entry point that handles routing and template rendering.

#### Key Routes:

- `/` (landing_page): Displays the welcome page with feature overview
- `/dashboard`: Shows real-time stock prices with currency conversions and recommendations
- `/search`: Handles stock ticker search functionality
- `/company/<ticker>`: Displays detailed company information and news

#### Notable Features:

- Custom datetime filter for Unix timestamp conversion
- Real-time currency conversion for stock prices
- Integration with Finnhub API for company data and news
- Responsive error handling for API failures

### Data Models

#### Stock Model (models/stock_model.py)

Handles stock price data persistence using Google Cloud Datastore.

```python
def save_stock_price(ticker, price):
    """Saves current stock prices to Datastore"""

def get_historical_prices(ticker, days=30):
    """Retrieves historical prices for analysis"""
```

#### Exchange Model (models/exchange_model.py)

Manages currency exchange rate data in Google Cloud Datastore.

```python
def save_exchange_rate(currency, rate):
    """Saves exchange rates for supported currencies"""
```

### Utility Modules

#### Stock Data (utils/stock_data.py)

Handles stock price data retrieval from Finnhub API.

**Features:**

- Tracks top 10 companies (AAPL, MSFT, GOOGL, etc.)
- Real-time price fetching
- Automatic data persistence
- Error handling for API failures

#### Currency Data (utils/currency_data.py)

Manages exchange rate data from Exchange Rate API V6.

**Supported Currencies:**

- USD (Base currency)
- EUR
- INR
- GBP

#### Analysis (utils/analysis.py)

Provides stock trend analysis and recommendations.

**Analysis Features:**

- 7-day moving average calculation
- Buy/Sell/Hold recommendations based on:
  - Current price vs. moving average
  - Price trend analysis
  - Historical data patterns

### Frontend Templates

#### Landing Page (templates/landing.html)

Welcome page introducing the dashboard features.

**Components:**

- Feature overview table
- Navigation to dashboard
- Responsive design elements

#### Dashboard (templates/dashboard.html)

Main data display interface.

**Features:**

- Real-time stock price display
- Multi-currency conversion
- Trading recommendations
- Search functionality
- Responsive table layout

#### Company Details (templates/company.html)

Detailed company information view.

**Displays:**

- Company profile
  - Industry classification
  - Market capitalization
  - Country of operation
  - Company website
- Recent news feed
- Historical data visualization

#### Search Page (templates/search.html)

Stock search interface.

**Features:**

- Ticker symbol search
- Form validation
- Direct navigation to company details

### Styling (static/styles.css)

**Key Style Components:**

- Responsive grid layouts
- Mobile-friendly design
- Consistent color scheme:
  - Primary: #f39c12 (Orange)
  - Secondary: Dark theme elements
  - Accent: #FF8C00 (Dark Orange)
- Custom table styling
- News article formatting
- Company profile card design

### API Integrations

#### Finnhub API

Used for retrieving:

- Real-time stock prices
- Company profiles
- Latest news articles
- Market data

**Endpoints Used:**

- `/quote`: Real-time stock quotes
- `/stock/profile2`: Company information
- `/company-news`: Latest news articles

#### Exchange Rate API (V6)

Used for currency conversion features.

**Implementation:**

- Real-time exchange rate updates
- Support for multiple currencies
- Rate caching in Datastore
- Automatic rate refresh

### Data Storage

#### Google Cloud Datastore

Used for persistent storage of:

- Historical stock prices
- Exchange rates
- Application data

**Entity Types:**

1. StockPrice
   - Properties: ticker, price, timestamp
2. ExchangeRate
   - Properties: currency, rate, timestamp

## Docker Deployment

1. Build the Docker image:

```bash
docker build -t stock-dashboard .
```

2. Run the container locally:

```bash
docker run -p 8080:8080 \
  -e FINNHUB_API_KEY=your_finnhub_api_key \
  -e EXCHANGE_RATE_API_KEY=your_exchange_rate_api_key \
  -e GOOGLE_CLOUD_PROJECT=your-gcp-project-id \
  -e PORT=8080 \
  stock-dashboard
```

## Google Cloud Deployment

### Setup GCP Project

1. Enable required APIs:

```bash
gcloud services enable \
  cloudbuild.googleapis.com \
  run.googleapis.com \
  artifactregistry.googleapis.com
```

2. Set your project ID:

```bash
PROJECT_ID=your-project-id
gcloud config set project $PROJECT_ID
```

### Deploy to Artifact Registry

1. Create a Docker repository:

```bash
gcloud artifacts repositories create stock-dashboard \
  --repository-format=docker \
  --location=us-west1 \
  --description="Stock Dashboard Container Repository"
```

2. Configure Docker authentication:

```bash
gcloud auth configure-docker us-west1-docker.pkg.dev
```

3. Tag and push the image:

```bash
docker tag stock-dashboard \
  us-west1-docker.pkg.dev/$PROJECT_ID/stock-dashboard/app:v1

docker push \
  us-west1-docker.pkg.dev/$PROJECT_ID/stock-dashboard/app:v1
```

### Deploy to Cloud Run

```bash
gcloud run deploy stock-dashboard \
  --image us-west1-docker.pkg.dev/$PROJECT_ID/stock-dashboard/app:v1 \
  --platform managed \
  --region us-west1 \
  --allow-unauthenticated \
  --set-env-vars "FINNHUB_API_KEY=your_finnhub_api_key,EXCHANGE_RATE_API_KEY=your_exchange_rate_api_key,GOOGLE_CLOUD_PROJECT=$PROJECT_ID"
```

## Environment Variables

| Variable              | Description                      |
| --------------------- | -------------------------------- |
| FINNHUB_API_KEY       | API key for Finnhub stock data   |
| EXCHANGE_RATE_API_KEY | API key for Exchange Rate API V6 |
| GOOGLE_CLOUD_PROJECT  | Your GCP project ID              |
| PORT                  | Port number (defaults to 8080)   |

## Project Structure

```
stock-dashboard/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── Dockerfile            # Container configuration
├── .env                  # Environment variables (not in git)
├── models/
│   ├── exchange_model.py # Exchange rate data model
│   └── stock_model.py    # Stock price data model
├── utils/
│   ├── analysis.py       # Trading analysis functions
│   ├── currency_data.py  # Exchange rate API integration
│   └── stock_data.py     # Stock price API integration
├── templates/
│   ├── landing.html      # Landing page template
│   ├── dashboard.html    # Main dashboard template
│   ├── search.html       # Search page template
│   └── company.html      # Company details template
└── static/
    └── styles.css        # Application styles
```

## Contributing

1. Fork the repository
2. Create a new branch
3. Make your changes
4. Submit a pull request
