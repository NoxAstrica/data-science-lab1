import requests
from typing import Dict

try:
    from .utils import save_to_json
except ImportError:
    from utils import save_to_json


def fetch_weather_data() -> Dict[str, any]:
    url = ("https://api.open-meteo.com/v1/forecast?latitude=35.6895&longitude=139.6917"
           "&daily=temperature_2m_max&timezone=Asia/Tokyo")

    response = requests.get(url, timeout=10)
    response.raise_for_status()
    data = response.json()
    
    date = data["daily"]["time"][0]
    max_temp = data["daily"]["temperature_2m_max"][0]
    return {"date": date, "max_temperature": max_temp}


if __name__ == "__main__":
    try:
        # Fetch the weather data
        weather_data = fetch_weather_data()

        # Save the data to a JSON file
        save_to_json(weather_data, "tokyo_weather.json")

        print("Data successfully saved to tokyo_weather.json")
    except Exception as e:
        print(f"An error occurred: {e}")
