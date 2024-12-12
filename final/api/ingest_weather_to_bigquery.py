from google.cloud import bigquery
import os

def load_weather_to_bigquery(csv_file):
    """Load historical weather data into BigQuery."""
    # Set the Google Cloud service account key
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "path/to/service_account.json"

    # Initialize BigQuery client
    client = bigquery.Client()

    # Define the BigQuery table
    table_id = "your_project_id.flight_data.weather"

    # Configure the load job
    job_config = bigquery.LoadJobConfig(
        source_format=bigquery.SourceFormat.CSV,
        skip_leading_rows=1,
        autodetect=True
    )

    # Load the data into BigQuery
    with open(csv_file, "rb") as source_file:
        load_job = client.load_table_from_file(source_file, table_id, job_config=job_config)

    # Wait for the job to complete
    load_job.result()
    print(f"Weather data from {csv_file} successfully loaded into {table_id}")

if __name__ == "__main__":
    load_weather_to_bigquery("sfo_hourly_weather.csv")
